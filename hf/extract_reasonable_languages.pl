#!/usr/bin/env perl


# my $MinNrSent    = 100;
my $MinNrSent    = 20;
my $MinBleuScore = 20;
my $MinChrFScore = 0.4;

my $header = '';

while (<>){
    if (/^\|\-\-/){
	$header .= '|----------'.$_;
	next;
    }
    next unless (/^\| /);
    my @cols = split(/\s*\|\s*/);
    shift(@cols);
    if ($cols[0] eq 'testset'){
	$header .= '| langpair '.$_;
	next;
    }
    if ($#cols > 3){
	next if ($cols[3] < $MinNrSent);
    }
    my @parts = split(/\./,$cols[0]);
    my $langpair = $parts[-1];
    my ($src,$trg) = split(/\-/,$langpair);
    s/\.$langpair / /;
    $benchmarks{$langpair} .= "| $langpair ".$_;

    next if ( ($cols[1] < $MinBleuScore) && ($cols[2] < $MinChrFScore) );
    $accepted{$langpair}++;
    $srclangs{$src}++ unless ($src eq 'multi');
    $trglangs{$trg}++ unless ($trg eq 'multi');
}

print join(' ',sort keys %srclangs),"\n";
print join(' ',sort keys %trglangs),"\n";
print "\n";

print $header;
foreach (sort keys %accepted){
    print $benchmarks{$_};
}

