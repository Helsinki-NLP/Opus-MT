#!/bin/env perl

use strict;

use vars qw($opt_l);
use Getopt::Std;
getopts('l:');

my $max = $opt_l || 100;

my $srcfile = shift(@ARGV);
my $trgfile = shift(@ARGV);
my $algfile = shift(@ARGV);


if ($srcfile=~/\.gz$/){
    open S,"gzip -cd <$srcfile |" || die "cannot open $srcfile";
}
else{ open S,"<$srcfile" || die "cannot open $srcfile"; }
if ($trgfile=~/\.gz$/){
    open T,"gzip -cd <$trgfile |" || die "cannot open $trgfile";
}
else{ open T,"<$trgfile" || die "cannot open $trgfile"; }
if ($algfile=~/\.gz$/){
    open A,"gzip -cd <$algfile |" || die "cannot open $algfile";
}
else{ open A,"<$algfile" || die "cannot open $algfile"; }


binmode(S,":utf8");
binmode(T,":utf8");
binmode(STDOUT,":utf8");


my $srcdoc = '<BEG> ';
my $trgdoc = '<BEG> ';
my $algdoc = '0-0';

my $srccount = 0;
my $trgcount = 0;
my $segcount = 0;

while (<S>){
    chomp;
    my $trg = <T>;
    my $alg = <A>;
    chomp($trg);
    chomp($alg);

    my @srctok = split(/\s+/);
    my @trgtok = split(/\s+/,$trg);

    if ( ($srccount+@srctok > $max) || ($trgcount+@trgtok > $max) ){
	$srcdoc .= '<BRK>';
	$trgdoc .= '<BRK>';
	$algdoc .= ' ';
	$algdoc .= $srccount+$segcount+1;
	$algdoc .= '-';
	$algdoc .= $trgcount+$segcount+1;
	print $srcdoc,"\t",$trgdoc,"\t",$algdoc,"\n";
	$srcdoc = '<CNT> ';
	$trgdoc = '<CNT> ';
	$algdoc = '0-0';
	$srccount = 0;
	$trgcount = 0;
	$segcount = 0;
    }
    if ( @srctok == 0 && @trgtok == 0 ){
	$srcdoc .= '<END>';
	$trgdoc .= '<END>';
	$algdoc .= ' ';
	$algdoc .= $srccount+$segcount+1;
	$algdoc .= '-';
	$algdoc .= $trgcount+$segcount+1;
	print $srcdoc,"\t",$trgdoc,"\t",$algdoc,"\n";
	$srcdoc = '<BEG> ';
	$trgdoc = '<BEG> ';
	$algdoc = '0-0';
	$srccount = 0;
	$trgcount = 0;
	$segcount = 0;
	next;
    }
    $srcdoc .= join(' ',@srctok);
    $trgdoc .= join(' ',@trgtok);
    $algdoc .= adjust_alignment($alg,$srccount,$trgcount,$segcount);
    $srcdoc .= ' <SEP> ';
    $trgdoc .= ' <SEP> ';
    $srccount += @srctok;
    $trgcount += @trgtok;
    $segcount++;
    $algdoc .= ' ';
    $algdoc .= $srccount+$segcount;
    $algdoc .= '-';
    $algdoc .= $trgcount+$segcount;
}

if ($srcdoc || $trgdoc){
    print $srcdoc,"\t",$trgdoc,"\n";
}


sub adjust_alignment{
    my ($alg,$srccount,$trgcount,$segcount) = @_;
    my @links = split(/\s+/,$alg);
    my @newLinks = ();
    foreach my $l (@links){
	my ($s,$t) = split(/\-/,$l);
	$s += $srccount+$segcount+1;
	$t += $trgcount+$segcount+1;
	push(@newLinks,$s.'-'.$t);
    }
    return ' '.join(' ',@newLinks) if (@newLinks);
    return '';
}
