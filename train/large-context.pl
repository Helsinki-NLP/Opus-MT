#!/bin/env perl

use vars qw($opt_l);
use Getopt::Std;
getopts('l:');

my $max = $opt_l || 100;

my $srcfile = shift(@ARGV);
my $trgfile = shift(@ARGV);

open S,"<$srcfile" || die "cannot open $srcfile";
open T,"<$trgfile" || die "cannot open $trgfile";

binmode(S,":utf8");
binmode(T,":utf8");
binmode(STDOUT,":utf8");


my $srcdoc = '<BEG> ';
my $trgdoc = '<BEG> ';

my $srccount = 0;
my $trgcount = 0;

while (<S>){
    chomp;
    my $trg = <T>;
    chomp($trg);
    my @srctok = split(/\s+/);
    my @trgtok = split(/\s+/,$trg);

    if ( ($srccount+@srctok > $max) || ($trgcount+@trgtok > $max) ){
	$srcdoc .= '<BRK>';
	$trgdoc .= '<BRK>';
	print $srcdoc,"\t",$trgdoc,"\n";
	$srcdoc = '<CNT> ';
	$trgdoc = '<CNT> ';
	$srccount = 0;
	$trgcount = 0;
    }
    if ( @srctok == 0 && @trgtok == 0 ){
	$srcdoc .= '<END>';
	$trgdoc .= '<END>';
	print $srcdoc,"\t",$trgdoc,"\n";
	$srcdoc = '<BEG> ';
	$trgdoc = '<BEG> ';
	$srccount = 0;
	$trgcount = 0;
	next;
    }
    $srcdoc .= join(' ',@srctok);
    $trgdoc .= join(' ',@trgtok);
    $srcdoc .= ' <SEP> ';
    $trgdoc .= ' <SEP> ';
    $srccount += @srctok;
    $trgcount += @trgtok;
}

if ($srcdoc || $trgdoc){
    print $srcdoc,"\t",$trgdoc,"\n";
}
