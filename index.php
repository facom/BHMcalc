<?PHP
//////////////////////////////////////////////////////////////////////////////////
//STATISTICS
//////////////////////////////////////////////////////////////////////////////////
if(!isset($_SESSION)){session_start();}
$sessid=session_id();
echo "<P STYLE=font-size:12px>Session $sessid</P>";

$PYTHONCMD="MPLCONFIGDIR=/tmp python";
$out=shell_exec("hostname");
if($out=="urania"){
  $WEBDIR="facom/pages/binary-habitability.rs/files/binary-habitabilitygovwk/.Interactive/BHMcalc";
  $DIR="/websites/sitios/$WEBDIR";
}else{
  $WEBDIR="BHMcalc";
  $DIR="/var/www/$WEBDIR";
}

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
<H1><A HREF="?">Binary Habitability Calculator</A><SUP style='color:red;font-size:18px'>v2.0</SUP>
<br/>
<a href=changeslog style=font-size:10px>Changeslog/</a><a href=TODO style=font-size:10px>ToDo</a>
</H1>

<form>
CONTENT;

//////////////////////////////////////////////////////////////////////////////////
//DEFAULT VALUES
//////////////////////////////////////////////////////////////////////////////////
$Z=0.0;
$FeH=0.0;
$M1=1.0;
$M2=0.5;
$Pbin=10.0;
$e=0.0;
$Mp=1.0;
$ap=1.5;
$ep=0.5;
$tau=1.0;
$tautot=2.0;
$incrit='recent venus';
$outcrit='early mars';

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

  //SAVE CONFIGURATION
  $fc=fopen("tmp/config-$sessid.log","w");
  fwrite($fc,"URL: $qstring\n\n");
  foreach(array_keys($_GET) as $field){
    $$field=$_GET[$field];
    $value=$$field;
    fwrite($fc,"$field=$value\n");
  }
  fclose($fc);
  
  if(!preg_match("/\w/",$qintegration)){$qintegration=0;}
  else{$qintegration=1;}
  if(!preg_match("/\w/",$qchz)){$qchz=0;}
  else{$qchz=1;}
  if($qintegration){$qchz=1;}

  if(!isset($stat) and !isset($back)){access("run");}
  if(!isset($reload)){
  $cmd="$PYTHONCMD BHMcalc.py $Z $M1 $M2 $e $Pbin $tau $Mp $ap $tautot $qintegration $sessid $zsvec $qchz $earlywind $FeH $ep '$incrit' '$outcrit' &> tmp/fulloutput-$sessid.log";
  exec($cmd,$output,$status); 
  shell_exec("echo '$cmd' > tmp/cmd-$sessid.log");
  $qreload="reload&$qstring";
  }else{
    $qreload=$qstring;
  }
  $result=shell_exec("cat tmp/output-$sessid.log");
  
  //ERROR
  if(preg_match("/ERROR/",$result)){
    echo "<P STYLE='color:red'>An error has occurred while executing the program</P>";
    echo "Executing: $cmd<br/>";
    echo "<pre style='background:yellow;padding:10px'>$result</pre>";
    echo "<a href=?back&$qstring>Back</a>";
    return;
  }

  $parts=preg_split("/\s+/",$result);
  echo "<a href=?back&$qstring>Back</a> - ";
  echo "<a href=?$qreload>Reload</a>";
  echo "<P><a href=tmp/fulloutput-$sessid.log target=_blank>Full Output</a> - <a href=tmp/config-$sessid.log target=_blank>Configuration</a> - <a href=tmp/cmd-$sessid.log target=_blank>Command</a></P>";

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
  $Z=$parts[$i++];

  $q=$M2/$M1;
  /*
  if($q>0){$type="Binary";}
  else{$type="Single star";}
  */
	
  $suffix=sprintf("%.2f%.2f%.3f%.2f-%s",$M1,$M2,$e,$Pbin,$sessid);

echo<<<CONTENT
<H2>Input</H2>
<table>
  <tr><td>Z:</td><td>$Z</td></tr>
  <tr><td>[Fe/H]:</td><td>$FeH</td></tr>
  <tr><td>M<sub>1</sub>:</td><td>$M1 M<sub>Sun</sub></td></tr>
  <tr><td>M<sub>2</sub>:</td><td>$M2 M<sub>Sun</sub></td></tr>
  <tr><td>q:</td><td>$q</td></tr>
  <tr><td>P<sub>bin</sub>:</td><td>$Pbin days</td></tr>
  <tr><td>e:</td><td>$e</td></tr>
  <tr><td>M<sub>p</sub>:</td><td>$Mp M<sub>Earth</sub></td></tr>
  <tr><td>a<sub>p</sub>:</td><td>$ap AU</td></tr>
  <tr><td>e<sub>p</sub>:</td><td>$ep</td></tr>
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
<H3>Habitable Zone</H3>
<a href="tmp/HZ-$suffix.png.txt" target="_blank"><img src="tmp/HZ-$suffix.png"></a><br/>
<a href="tmp/HZ+planet-$suffix.png.txt" target="_blank"><img src="tmp/HZ+planet-$suffix.png"></a><br/>
CONTENT;

if($qchz){
$tsys=$parts[$i++];
$lincont=$parts[$i++];$loutcont=$parts[$i++];
$slincont=$parts[$i++];$sloutcont=$parts[$i++];
echo<<<CONTENT
<H3>Continuous Habitable Zone</H3>
<table>
  <tr><td>&tau;<sub>sys</sub>:</td><td>$tsys Gyr</td></tr>
  <tr><td>CHZ:</td><td>[$lincont,$loutcont] AU</td></tr>
  <tr><td>CHZ single-primary:</td><td>[$lincont,$loutcont] AU</td></tr>
</table>
<a href="tmp/HZevol-$suffix.png.txt" target="_blank"><img src="tmp/HZevol-$suffix.png"></a><br/>
CONTENT;
}
if($qintegration){
$suffix1=sprintf("%.2f",$M1);
$suffix2=sprintf("%.2f",$M2);
echo<<<CONTENT
<H3>Evolution Plots</H3>

Evolution of rotational periods with (solid) and without (dashed)
tidal interaction:<br/>

<a href="tmp/PeriodEvolution-$suffix.png.txt" target="_blank"><img src="tmp/PeriodEvolution-$suffix.png"></a><br/>

Evolution of XUV and stellar wind flux within the continuous habitable
zone in Binary with BHM (solid), no BHM (dash-dotted) and
single-primary (dotted): <br/>

<a href="tmp/FluxXUV-$suffix.png.txt" target="_blank"><img src="tmp/FluxXUV-$suffix.png"></a><br/> 

<a href="tmp/FluxSW-$suffix.png.txt" target="_blank"><img src="tmp/FluxSW-$suffix.png"></a><br/>

Ratio of XUV and stellar wind flux in Binaries with BHM, without BHM
and around single-primary systems:<br/>

<a href="tmp/RatiosFluxXUV-$suffix.png.txt" target="_blank"><img src="tmp/RatiosFluxXUV-$suffix.png"></a><br/> 

<a href="tmp/RatiosFluxSW-$suffix.png.txt" target="_blank"><img src="tmp/RatiosFluxSW-$suffix.png"></a><br/>

Integrated XUV and stellar wind fluxes:<br/>

<a href="tmp/IntFXUV-$suffix.png.txt" target="_blank"><img src="tmp/IntFXUV-$suffix.png"></a><br/>
<a href="tmp/IntFSW-$suffix.png.txt" target="_blank"><img src="tmp/IntFSW-$suffix.png"></a><br/>

Mass-loss as a function of planetary mass at the inner edge of the
continuous habitable zone:<br/>

<a href="tmp/MassLoss-$suffix.png.txt" target="_blank"><img src="tmp/MassLoss-$suffix.png"></a><br/>

<!--DEPRECATED
<img src="tmp/PeriodFit-$suffix1.png"><br/>
<img src="tmp/PeriodFit-$suffix2.png"><br/>
<img src="tmp/AccelerationEvolution-$suffix.png"><br/>
-->

CONTENT;
}

echo<<<CONTENT
<a href=?back&$qstring>Back</a> - <a href=?$qreload>Reload</a>
CONTENT;

 }else{

//////////////////////////////////////////////////////////////////////////////////
//INPUT
//////////////////////////////////////////////////////////////////////////////////
   if(!isset($stat) and !isset($back)){access("access");}

echo<<<CONTENT
<H2>Input Data</H2>

<input type="submit" name="submit" value="submit">

<H3>Binary System</H3>

Z : <input type="text" name="Z" value="$Z"><br/> 

<i style="font-size:12px">Metallicity of the binary system.  If
unknown leave [Fe/H] below in 0.  Theoretical metallicities are in the
  range 0.0001 to 0.06 (see isochrone set in the behavior section).  If you only know [Fe/H] leave Z =
0</i><br/><br/>

[Fe/H] : <input type="text" name="FeH" value="$FeH"><br/> 

<i style="font-size:12px">Metallicity in dex.</i><br/><br/>

M<sub>1</sub> : <input type="text" name="M1" value="$M1"> M<sub>Sun</sub><br/>
<i style="font-size:12px">Mass of the main component</i><br/><br/>

M<sub>2</sub> : <input type="text" name="M2" value="$M2"> M<sub>Sun</sub><br/>
<i style="font-size:12px">Mass of the secondary component.  Leave 0 to compute single star properties</i><br/><br/>

P<sub>bin</sub> : <input type="text" name="Pbin" value="$Pbin"> days<br/>
<i style="font-size:12px">Binary period.</i><br/><br/>

e : <input type="text" name="e" value="$e"><br/>
<i style="font-size:12px">Binary eccentricity.</i><br/><br/>

<H3>Planet (optional)</H3>

M<sub>p</sub> : <input type="text" name="Mp" value="$Mp"> M<sub>Earth</sub><br/>
<i style="font-size:12px">Planetary mass. Values must be between 0.5 and 10.0</i><br/><br/>

a<sub>p</sub> : <input type="text" name="ap" value="$ap"> AU<br/>
<i style="font-size:12px">Semimajor axis of planet</i><br/><br/>

e<sub>p</sub> : <input type="text" name="ep" value="$ep"><br/>
<i style="font-size:12px">Eccentricity of the planet</i><br/><br/>

<H3>Planetary System (optional)</H3>

&tau; : <input type="text" name="tau" value="$tau"> Gyr<br/>
<i style="font-size:12px">Age of the system.  Values must be between 0.01 and 12.5 Gyr</i><br/><br/>

<H3>Continuous Habitable Zone (CHZ, Optional)</H3>

Compute the continuous HZ:<input type="checkbox" name="qchz"><br/>

<H3>Integration (optional)</H3>

Integrate:<input type="checkbox" name="qintegration"><br/>

Total integration time : <input type="text" name="tautot" value="$tautot"> Gyr<br/>
<i style="font-size:12px">Values must be between 0.01 and 12.5 Gyr</i><br/><br/>

<H3>Behavior</H3>

Set of isochrones : 
<select name="zsvec">
  <option value="ZSVEC_full">Full (35 metallicities, 0.0001-0.06, [Fe/H] -2.30 to 0.62)</option>
  <option value="ZSVEC_coarse">Coarse (10 values, 0.0001-0.06, [Fe/H] -2.30 to 0.62)</option>
  <option value="ZSVEC_siblings" selected>Near solar (3 values , 0.01-0.02, [Fe/H] -0.197 to 0.117)</option>
</select><br/>
<i style="font-size:12px">It could reduce considerably the execution time.</i><br/><br/>

Type of early stellar wind : 
<select name="earlywind">
<option value="trend" selected>Trending</option>
<option value="constant">Constant</option>
</select><br/>

<i style="font-size:12px">Observations does not provide us information
about the stellar wind before &tau;<0.7 Gyr.  Some observations
suggest there is a saturation on magnetic activity before that.
Select which type of behavior do you want to simulate.</i><br/><br/>

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
