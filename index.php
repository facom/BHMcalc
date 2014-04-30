<?PHP
//////////////////////////////////////////////////////////////////////////////////
//STATISTICS
//////////////////////////////////////////////////////////////////////////////////
$PYTHONCMD="MPLCONFIGDIR=/tmp python";
$WEBDIR="facom/pages/binary-habitability.rs/files/binary-habitabilitygovwk/.Interactive/BHM-Calculator";
$DIR="/websites/sitios/$WEBDIR";

function access($referer){
  global $DIR,$WEBDIR;

  date_default_timezone_set("EST");
  $PhpGlobal["TODAY"]=getdate();
  $PhpGlobal["YEAR"]=$PhpGlobal["TODAY"]['year'];//e.g. 2005
  $PhpGlobal["MONTH"]=100+$PhpGlobal["TODAY"]['mon'];
  $PhpGlobal["MONTH"]=substr($PhpGlobal["MONTH"],1,2);//e.g. 01, 12
  $PhpGlobal["DAY"]=$PhpGlobal["TODAY"]['mday'];//e.g. 12, 31
  $PhpGlobal["DATE"]="$PhpGlobal[DAY]-$PhpGlobal[MONTH]-$PhpGlobal[YEAR]";//e.g. 12-02-2005
  $date=$PhpGlobal["TODAY"]['hours']."-".$PhpGlobal["DATE"];
  $agent=$_SERVER["HTTP_USER_AGENT"];
  $remote=$_SERVER["REMOTE_ADDR"];
  $self=$_SERVER["PHP_SELF"];
  $hitstr="$date**$remote**$referer**$self**$agent\n";
  $logfile="$DIR/access.log";
  if(file_exists($logfile)){
    $fl=fopen($logfile,"a");
  }else{
    $fl=fopen($logfile,"w");
  }
  fwrite($fl,$hitstr);
  fclose($fl);
}

//////////////////////////////////////////////////////////////////////////////////
//FOOTER
//////////////////////////////////////////////////////////////////////////////////
echo<<<CONTENT
<HTML>
<BODY>
<H1>Binary Habitability
Calculator<SUP style='color:red;font-size:18px'>v2.0</SUP></H1>

<form>
CONTENT;

//////////////////////////////////////////////////////////////////////////////////
//DEFAULT VALUES
//////////////////////////////////////////////////////////////////////////////////
$Z=0.0152;
$M1=1.0;
$M2=0.5;
$Pbin=10.0;
$e=0.0;
$Mp=1.0;
$ap=1.5;
$tau=1.0;
$tautot=4.6;

//////////////////////////////////////////////////////////////////////////////////
//COMMON
//////////////////////////////////////////////////////////////////////////////////
foreach(array_keys($_GET) as $field){
    $$field=$_GET[$field];
}
foreach(array_keys($_POST) as $field){
    $$field=$_POST[$field];
}

//////////////////////////////////////////////////////////////////////////////////
//REPORT
//////////////////////////////////////////////////////////////////////////////////
if(isset($submit) and !isset($back)){
  $qstring=$_SERVER["QUERY_STRING"];
  if(!isset($stat) and !isset($back)){access("run");}
  if(!isset($reload)){
  $cmd="$PYTHONCMD BHMcalc.py $Z $M1 $M2 $e $Pbin $tau $Mp $ap $tautot > tmp/fulloutput.log";
  shell_exec($cmd);
  $qreload="reload&$qstring";
  }else{
    $qreload=$qstring;
  }
  $result=shell_exec("cat tmp/output.log");
  /*
  echo "Executing: $cmd<br/>";
  echo "<pre>$result</pre>";
  //*/

  $parts=preg_split("/\s+/",$result);
  echo "<a href=?back&$qstring>Back</a> - ";
  echo "<a href=?$qreload>Reload</a>";
  echo "<P><a href=tmp/fulloutput.log>Full Output</a></P>";

  //print_r($parts);

  //BASIC INFORMATION ON THE SYSTEM
  $i=0;
  $g1=$parts[$i++];$T1=$parts[$i++];$R1=$parts[$i++];$L1=$parts[$i++];
  $Rmin1=$parts[$i++];$Rmax1=$parts[$i++];$Pini1=$parts[$i++];$Prot1=$parts[$i++];
  $lin1=$parts[$i++];$aE1=$parts[$i++];$aHZ1=$parts[$i++];$lout1=$parts[$i++];
  $g2=$parts[$i++];$T2=$parts[$i++];$R2=$parts[$i++];$L2=$parts[$i++];
  $Rmin2=$parts[$i++];$Rmax2=$parts[$i++];$Pini2=$parts[$i++];$Prot2=$parts[$i++];
  $lin2=$parts[$i++];$aE2=$parts[$i++];$aHZ2=$parts[$i++];$lout2=$parts[$i++];
  $abin=$parts[$i++];$acrit=$parts[$i++];$nsync=$parts[$i++];$Psync=$parts[$i++];
  $lin=$parts[$i++];$aE=$parts[$i++];$aHZ=$parts[$i++];$lout=$parts[$i++];
  $tsync1=$parts[$i++];$tsync2=$parts[$i++];

  $q=$M2/$M1;
  if($q>0){$type="Binary";}
  else{$type="Single star";}
	
  $suffix=sprintf("%.2f%.2f%.3f%.2f",$M1,$M2,$e,$Pbin);

echo<<<CONTENT
<H2>Input</H2>
<table>
  <tr><td>Type:</td><td>$type</td></tr>
  <tr><td>M<sub>1</sub>:</td><td>$M1 M<sub>Sun</sub></td></tr>
  <tr><td>M<sub>2</sub>:</td><td>$M2 M<sub>Sun</sub></td></tr>
  <tr><td>q:</td><td>$q</td></tr>
  <tr><td>P<sub>bin</sub>:</td><td>$Pbin days</td></tr>
  <tr><td>e:</td><td>$e</td></tr>
  <tr><td>M<sub>p</sub>:</td><td>$Mp M<sub>Earth</sub></td></tr>
  <tr><td>a<sub>p</sub>:</td><td>$ap AU</td></tr>
  <tr><td>&tau;:</td><td>$tau Gyr</td></tr>
</table>

<H2>Binary System Properties</H2>
<table>
  <tr><td>a<sub>bin</sub>:</td><td>$abin AU</td></tr>
  <tr><td>a<sub>crit</sub>:</td><td>$acrit AU</td></tr>
  <tr><td>n<sub>sync</sub>=&Omega;/n:</td><td>$nsync</td></tr>
  <tr><td>P<sub>sync</sub>=n<sub>sync</sub>P<sub>bin</sub></td><td>$Psync</td></tr>
  <tr><td>a<sub>in</sub>:</td><td>$lin AU</td></tr>
  <tr><td>a<sub>HZ</sub>:</td><td>$aHZ AU</td></tr>
  <tr><td>a<sub>out</sub>:</td><td>$lout AU</td></tr>
  <tr><td>t<sub>sync1</sub>:</td><td>$tsync1 Gyr</td></tr>
  <tr><td>t<sub>sync2</sub>:</td><td>$tsync2 Gyr</td></tr>
</table>

<H2>Instantaneous Stellar Properties</H2>
<P>The following properties of the stars as measured at &tau;=$tau
Gyr.</P>
<H3>Main Component</H3>
<table>
  <tr><td>M:</td><td>$M1 M<sub>sun</sub></td></tr>
  <tr><td>g:</td><td>$g1 cm/s<sup>2</sup></td></tr>
  <tr><td>T<sub>eff</sub>:</td><td>$T1 K</td></tr>
  <tr><td>R:</td><td>$R1 R<sub>sun</sub> (Range in &tau;=0.01-$tau Gyr: $Rmin1-$Rmax1 R<sub>sun</sub>)</td></tr>
  <tr><td>L:</td><td>$L1 L<sub>sun</sub></td></tr>
  <tr><td>P<sub>rot</sub>:</td><td>$Prot1 days</td></tr>
  <tr><td>HZ:</td><td>[$lin1,$aE1 ($aHZ1),$lout1] AU</td></tr>
</table>
<H3>Secondary Component</H3>
<table>
  <tr><td>M:</td><td>$M2 M<sub>sun</sub></td></tr>
  <tr><td>g:</td><td>$g2 cm/s<sup>2</sup></td></tr>
  <tr><td>T<sub>eff</sub>:</td><td>$T2 K</td></tr>
  <tr><td>R:</td><td>$R2 R<sub>sun</sub> (Range in &tau;=0.01-$tau Gyr: $Rmin2-$Rmax2 R<sub>sun</sub>)</td></tr>
  <tr><td>L:</td><td>$L2 L<sub>sun</sub></td></tr>
  <tr><td>P<sub>rot</sub>:</td><td>$Prot2 days</td></tr>
  <tr><td>HZ:</td><td>[$lin2,$aE2 ($aHZ2),$lout2] AU</td></tr>
</table>
<br/>
<a href=?back&$qstring>Back</a> - <a href=?$qreload>Reload</a>
<H3>Plots</H3>
<img src="tmp/PeriodEvolution-$suffix.png"><br/>
<img src="tmp/AccelerationEvolution-$suffix.png"><br/>
<img src="tmp/FluxXUV-$suffix.png"><br/>
<img src="tmp/FluxSW-$suffix.png"><br/>
CONTENT;
 }else{

//////////////////////////////////////////////////////////////////////////////////
//INPUT
//////////////////////////////////////////////////////////////////////////////////
   if(!isset($stat) and !isset($back)){access("access");}
echo<<<CONTENT
<H2>Input Data</H2>

<H3>Binary System</H3>

Z : <input type="text" name="Z" value="$Z"><br/>
<i style="font-size:12px">Metallicity of the system.  If unknown leave the solar metallicity Z = 0.0152.  Theoretical metallicities are in the range 0.0001 to 0.06</i><br/><br/>

M<sub>1</sub> : <input type="text" name="M1" value="$M1"> M<sub>Sun</sub><br/>
<i style="font-size:12px">Mass of the main component</i><br/><br/>

M<sub>2</sub> : <input type="text" name="M2" value="$M2"> M<sub>Sun</sub><br/>
<i style="font-size:12px">Mass of the secondary component.  Leave 0 to compute single star properties</i><br/><br/>

P<sub>bin</sub> : <input type="text" name="Pbin" value="$Pbin"> days<br/>
<i style="font-size:12px">Binary period.</i><br/><br/>

e : <input type="text" name="e" value="$e"><br/>
<i style="font-size:12px">Binary eccentricity.</i><br/><br/>

<input type="submit" name="submit" value="submit">

<H3>Planet (optional)</H3>

M<sub>p</sub> : <input type="text" name="Mp" value="$Mp"> M<sub>Earth</sub><br/>
<i style="font-size:12px">Planetary mass. Values must be between 0.5 and 10.0</i><br/><br/>

a<sub>p</sub> : <input type="text" name="ap" value="$ap"> AU<br/>
<i style="font-size:12px">Semimajor axis of planet</i><br/><br/>

<input type="submit" name="submit" value="submit">

<H3>Planetary System (optional)</H3>

&tau; : <input type="text" name="tau" value="$tau"> Gyr<br/>
<i style="font-size:12px">Age of the system.  Values must be between 0.01 and 13.0 Gyr</i><br/><br/>

<H3>Integration (optional)</H3>

Total integration time : <input type="text" name="tautot" value="$tautot"> Gyr<br/>
<i style="font-size:12px">Values must be between 0.01 and 13.0 Gyr</i><br/><br/>

<input type="submit" name="submit" value="submit">
CONTENT;
 }

//////////////////////////////////////////////////////////////////////////////////
//FOOTER
//////////////////////////////////////////////////////////////////////////////////
if(isset($stat)){
echo<<<CONTENT
<h2>Usage statistics</h2>
<a href="http://astronomia.udea.edu.co/sitios/$WEBDIR/access.log" target="_blank">
Full
</a>
 - 
<a href="http://urania.udea.edu.co/sitios/facom/cgi-bin/stat.php?statfile=$DIR/access.log" target="_blank">
Recalculate
</a> - 
<a href="http://astronomia.udea.edu.co/sitios/$WEBDIR/access.html" target="_blank">
Last
</a>
CONTENT;
}

echo<<<CONTENT
</form>
<hr/>

<i style="font-size:10pt">
Developed by Jorge Zuluaga (2014), Viva la BHM!. <br/> 
Last update: 30-April-2014 (Jorge Zuluaga)<br/>
Please cite: Mason, P. A., Zuluaga, J. I., Clark, J. M., &
Cuartas-Restrepo, P. A. (2013). Rotational Synchronization May Enhance
Habitability for Circumbinary Planets: Kepler Binary Case Studies. The
Astrophysical Journal Letters, 774(2), L26.  </i>

</BODY>
</HTML>
CONTENT;
?>
