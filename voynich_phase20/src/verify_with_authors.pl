#!/usr/bin/env perl
# CC BY-SA 4.0; see ../README.md for attribution and scope.
use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/../vendor/hhk-decipherment";
use JSON::PP;
use NoSpace;
use JMSmoothing;

sub read_json {
    open my $f, '<', $_[0] or die $!;
    local $/;
    return decode_json(<$f>);
}
my ($tables_path, $patterns_path, $audit_path) = @ARGV;
die "Expected reduced tables, original patterns, audit JSON\n" unless $audit_path;
my $reduced = read_json($tables_path);
my %tables;
for my $unit (qw(word char)) {
    for my $n (1..3) {
        my %table;
        for my $row (@{$reduced->{"$unit$n"}}) {
            my @tokens = split /\t/, $row->[0];
            my $target = \%table;
            for my $i (0..$n-2) {
                $target->{$tokens[$i]} //= {};
                $target = $target->{$tokens[$i]};
            }
            $target->{$tokens[-1]} = $row->[1];
        }
        $tables{"$unit$n"} = \%table;
    }
}
my (%vocab, $maxlen);
$maxlen = 0;
open my $patterns, '<', $patterns_path or die $!;
while (<$patterns>) {
    chomp;
    my ($order, $pattern, @words) = split /\t/;
    next unless $order == 1;
    for my $word (@words) {
        $vocab{$word} = 1;
        $maxlen = length($word) if length($word) > $maxlen;
    }
}
close $patterns;
my @cl = (0.0950848948641174, 0.229797965264228, 0.675117139871655);
my @wl = (0.129793302623898, 0.226872659329747, 0.643334038046355);
sub score {
    return JMSmoothing::ProbCharWord($_[0], @tables{qw(char1 char2 char3 word1 word2 word3)}, @cl, @wl, 0.05);
}
my $audit = read_json($audit_path);
my @rows;
for my $row (@{$audit->{rows}}) {
    my $greedy = NoSpace::FindWords($row->{letters}, \%vocab, $maxlen);
    push @rows, {
        candidate => $row->{candidate},
        greedy_segmentation => $greedy,
        greedy_score_ln => score($greedy),
        exact_segmentation => $row->{exact}{segmentation},
        exact_score_ln => score($row->{exact}{segmentation}),
    };
}
print JSON::PP->new->canonical->pretty->encode({
    vocabulary_size => scalar keys %vocab,
    scope => 'Unmodified upstream greedy segmenter and scorer; selected probability tables, full published unigram vocabulary.',
    rows => \@rows,
});
