#!/usr/bin/env perl

my $MinBleuTatoeba = 20;
my $MinBleu = 10;

my %results = ();
while (<>){
    my ($langpair, $testset, $chrf, $bleu) = split(/\t/);
    if ($testset=~/tatoeba-test-(.*)$/i){
	next unless ($bleu >= $MinBleuTatoeba);
    }
    else{
	next unless ($bleu >= $MinBleu);
    }	
    my $version - undef;
    next if ($testset eq 'flores101-dev');
    next if ($testset=~'newssyscomb');
    next if ($testset=~'newstestB');

    my $name = $testset;
    if ($testset=~/tatoeba-test-(.*)$/i){
	$version = ' '.$1;
	$testset = 'tatoeba_mt';
    }
    # $testset=~s/^news/WMT-news/;
    $testset=~s/^newstest(20[0-9]{2}).*/wmt-$1-news/;
    $testset=~s/^multi30k_test_(.*)$/multi30k-$1/;

    if ($testset=~s/^flores101-(devtest|dev)$/flores_101/){
	my ($src,$trg) = split(/\-/,$langpair);
	$results{$testset}{$langpair}[1] = "$src $trg $1"
    }
    else{
	$results{$testset}{$langpair}[1] = $langpair;
    }

    $results{$testset}{$langpair}[0] = $name;    
    $results{$testset}{$langpair}[2] = $bleu;
    $results{$testset}{$langpair}[3] = $chrf;
}

foreach my $t (sort keys %results){
    foreach my $l (sort keys %{$results{$t}}){
	print "  - task:\n";
	print "      name: Translation $l\n";
	print "      type: translation\n";
	print "      args: $l\n";
	print "    dataset:\n";
	print "      name: $results{$t}{$l}[0]\n";
	print "      type: $t\n";
	#	print "      args: $l $results{$t}{$l}[1]\n";
	#	print "      args: $l\n";
	print "      args: $results{$t}{$l}[1]\n";
	print "    metrics:\n";
	print "       - name: BLEU\n";
	print "         type: bleu\n";
	print "         value: $results{$t}{$l}[2]\n";
	print "       - name: chr-F\n";
	print "         type: chrf\n";
	print "         value: $results{$t}{$l}[3]\n";
    }
}
