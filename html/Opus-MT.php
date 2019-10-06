<?php

echo '<h1>OPUS-MT</h1>';

?>
OPUS-MT provides pre-trained neural translation models trained on <a href="http://opus.nlpl.eu">OPUS data</a>. These models can seamlessly run with the OPUS-MT transation servers that can be installed from our <a href="https://github.com/Helsinki-NLP/OPUS-MT">OPUS-MT github repository</a>.
<?php

$baseUrl = 'https://object.pouta.csc.fi/OPUS-MT';
$xmlstring = file_get_contents($baseUrl);

$xml = simplexml_load_string($xmlstring);
$json = json_encode($xml);
$array = json_decode($json,TRUE);

$modelDate = array();

foreach ($array['Contents'] as &$m){

  if (!strpos($m['Key'],'zip')){
      continue;
  }

  $pieces = explode('/', $m['Key']);
  $langs = explode('-', $pieces[1]);

  $newModel = true;
  if (array_key_exists($langs[0],$modelDate)){
    if (array_key_exists($langs[1],$modelDate[$langs[0]])){
      if ($m['LastModified'] < $modelDate[$langs[0]][$langs[1]]){
	$newModel = false;
      }
    }
  }

  if ($newModel){
    if (strpos($langs[0],'+') or strpos($langs[1],'+')){
      $multiModels[$langs[0]][$langs[1]]['file'] = $m['Key'];
      $multiModels[$langs[0]][$langs[1]]['size'] = $m['Size'];
    }
    else{
      $singleModels[$langs[0]][$langs[1]]['file'] = $m['Key'];
      $singleModels[$langs[0]][$langs[1]]['size'] = $m['Size'];
    }
    $modelDate[$langs[0]][$langs[1]] = $m['LastModified'];
  }
}

echo '<h2>Pre-Trained Bilingual NMT Models</h2>';

echo 'List of bilingual models sorted by source language. Download a zip file by clicking on the linked target language:';

ksort($singleModels);
echo '<ul>';
foreach ($singleModels as $src => $srcModels){
  echo '<li><b>'.$src.'</b>: ';
  ksort($srcModels);
  foreach ($srcModels as $trg => $trgModels){
    echo '[<a href="'.$baseUrl.'/'.$trgModels['file'].'">'.$trg.'</a>]';
  }
  echo '</li>';
}
echo '</ul>';



echo '<h2>Pre-Trained Multilingual NMT Models</h2>';

echo 'List of multilingual models sorted by the set of source languages. The languages that are supported are separated by "+". Download the zip files by clicking on the linked target language set:';

ksort($multiModels);
echo '<ul>';
foreach ($multiModels as $src => $srcModels){
  echo '<li><b>'.$src.'</b>: ';
  ksort($srcModels);
  foreach ($srcModels as $trg => $trgModels){
    echo '[<a href="'.$baseUrl.'/'.$trgModels['file'].'">'.$trg.'</a>]';
  }
  echo '</li>';
}
echo '</ul>';


echo '<h2>NMT Benchmark Scores</h2>';

echo '<p>Latest benchmark results (Note: may currently not match the models above):</p>';

$scores = file_get_contents($baseUrl.'/scores.txt');

/*
echo "<pre>";
echo $scores;
echo "</pre>";
*/

$scores = preg_replace('/\(\S+\)/','',$scores);
$scores = str_replace('/','</td><td>',$scores);
$scores = str_replace('-','</td><td>',$scores);
$scores = preg_replace('/ {4,}/','</td><td>',$scores);
$scores = str_replace("\n",'</td></tr><tr><td>',$scores);

echo '<table><tr><th>source language(s)</th><th>target language(s)</th><th>test set</th><th>BLEU</th><th>METEOR</th><th>TER</th><th>LENGTH</th></tr>';
echo '<tr><td>';
echo $scores;
echo '</td></tr></table>';


/*
echo "<pre>";
var_dump($array['Contents']);
echo "</pre>";
*/

?>
<h3>TODO</h3>

<ul>
<li>Downloadable OPUS-MT server image</li>
<li>Downloadable OPUS-MT docker container</li>
<li>Download links of alternative / old models</li>
<li>Reliable benchmarks of all models</li>
<li>Downloadable test set translations</li>
</ul>
