<?PHP
/*
###################################################
#  ____  _    _ __  __           _      
# |  _ \| |  | |  \/  |         | |     
# | |_) | |__| | \  / | ___ __ _| | ___ 
# |  _ <|  __  | |\/| |/ __/ _` | |/ __|
# | |_) | |  | | |  | | (_| (_| | | (__ 
# |____/|_|  |_|_|  |_|\___\__,_|_|\___|
# v2.0
###################################################
# 2014 [)] Jorge I. Zuluaga, Viva la BHM!
###################################################
# Web Interface
###################################################
*/
$QMAINTAINANCE="block";
//$QMAINTAINANCE="none";
include_once("web/BHM.php");
?>
<?PHP
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//COMMON CONTENT
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$BHMcalc="<b style='font-family:Courier;color:red'>BHMcalc</b>";

//////////////////////////////////////////////////////////////////////////////////
//LOAD A CONFIGURATION
//////////////////////////////////////////////////////////////////////////////////
if(isset($LOADCONFIG)){
  $stdout="BHMrun-load-$SESSID";
  $stderr="BHMrun-load-$SESSID";
  $cmd="$PYTHONCMD BHMrun.py - $SESSDIR \"$QUERY_STRING\"";
  $out=shell_exec($cmd." 2> $TMPDIR/$stderr |tee $TMPDIR/$stdout");
  $header=mainHeader("1","?Modes=$Modes");
  echo "$header<body>Loading $Modes configuration...</body>";
  return;
}
accessLog("browse");

//////////////////////////////////////////////////////////////////////////////////
//INTERFACE SELECTION
//////////////////////////////////////////////////////////////////////////////////
$TABID=0;
$QCALCMODE=0;
$updateall="";
$tabs="";
$main="";
$help="";
$summary="";
if(!isset($Modes)){$Modes="Basic";}
$oModes=$Modes;
if($Modes=="Binary"){$Modes="Star1:Star2:Planet:$Modes";}
if($Modes=="Habitability"){$Modes="Star1:Star2:Planet:Binary:$Modes";}
if($Modes=="Interactions"){$Modes="Star1:Star2:Planet:Binary:Habitability:$Modes";}

//////////////////////////////////////////////////////////////////////////////////
//SESSION DIRECTORY
//////////////////////////////////////////////////////////////////////////////////
if(!is_dir($SESSIONDIR)){
  $source_dir=$SYSDIR."/template";
  echoVerbose("No session directory.");
  $qdir="No session directory.";
  if(!isset($TABID)){$TABID=0;}
}else{
  $source_dir=$SESSIONDIR;
  echoVerbose("Session directory already exist.");
  $qdir="Existing session directory.";
  if(!isset($TABID)){$TABID=2;}
}

//////////////////////////////////////////////////////////////////////////////////
//ACTIVE CODE
//////////////////////////////////////////////////////////////////////////////////

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//READING CONFIGURATION FILES
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//*
loadConfiguration("$source_dir/star1.conf","star1");
loadConfiguration("$source_dir/star2.conf","star2");
loadConfiguration("$source_dir/binary.conf","binary");
loadConfiguration("$source_dir/hz.conf","hz");
loadConfiguration("$source_dir/rotation.conf","rotation");
loadConfiguration("$source_dir/planet.conf","planet");
loadConfiguration("$source_dir/interaction.conf","interaction");
//*/

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//ADJUST VALUES
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$planet_Morb=$star1_M+$star2_M;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//AJAX FORM
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//CATALOGUE
$codecat=ajaxMultipleForm(array("cat"),"cat_form");
$ajaxform_cat_Update=ajaxFromCode($codecat,"'#cat_Update'","click");

//STAR1
$code=ajaxMultipleForm(array("star1"),"star1_form");
$ajaxform_star1_Update=ajaxFromCode($code,"'#star1_Update'","click");

//STAR2
$code=ajaxMultipleForm(array("star2"),"star2_form");
$ajaxform_star2_Update=ajaxFromCode($code,"'#star2_Update'","click");

//PLANET
$code=ajaxMultipleForm(array("planet"),"planet_form");
$ajaxform_planet_Update=ajaxFromCode($code,"'#planet_Update'","click");

//BINARY
$code=ajaxMultipleForm(array("binary"),"binary_form");
$ajaxform_binary_Update=ajaxFromCode($code,"'#binary_Update'","click");

//HABITABLE ZONE
$code=ajaxMultipleForm(array("hz"),"hz_form");
$ajaxform_hz_Update=ajaxFromCode($code,"'#hz_Update'","click");

//ROTATION
$code=ajaxMultipleForm(array("rotation"),"rotation_form");
$ajaxform_rotation_Update=ajaxFromCode($code,"'#rotation_Update'","click");

//INTERACTION
$code=ajaxMultipleForm(array("interaction"),"interaction_form");
$ajaxform_interaction_Update=ajaxFromCode($code,"'#interaction_Update'","click");

//SUMMARY
$code=ajaxMultipleForm(array("summary"),"summary_form");
$ajaxform_summary_Update=ajaxFromCode($code,"'#summary_Update'","click");
$ajax_summary_Load=ajaxFromCode($code,"document","ready");

//UPDATE ALL
if(isset($LOAD)){$slope=1.0;}
else{$slope=1.0;}
$code=ajaxMultipleForm(array("interaction","rotation","hz",
			     "binary","star1","star2","planet","summary"),"allforms",$slope);
$ajax_all_Update=ajaxFromCode($code,"'#all_Update'","click");
$ajax_all_Load=ajaxFromCode($code,"document","ready");

//BUG REPORT
$codebug=ajaxMultipleFormSimple("bug_form","bug_result");
$ajax_bug=ajaxFromCode($codebug,"\"#bug_send\"","click");

//LOAD CATALOGUE
$ajax_cat_Load=ajaxFromCode($codecat,"document","ready");

//FORCE UPDATE
$force_update=<<<F
  <input class="qover" type="hidden" name="qover" value="0">
  <a href="JavaScript:void(0)" class="force" onclick="forceUpdate('.force','.qover')">Smart</a> 
F;

$changeFeH=<<<C
  changeAjax('$wDIR/BHMutil.php?ACTION=Metals&ZtoFeH','.star_Z','.star_FeH');
C;
$changeZ=<<<C
  changeAjax('$wDIR/BHMutil.php?ACTION=Metals&FeHtoZ','.star_FeH','.star_Z');
C;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//CODE TO EXECUTE WHEN DOCUMENT IS READY
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$document_load=<<<C
<script>
  $(document).ready(function(){
      $changeZ
      changeValues(['.star_Z'],'input[name=star1_Z]');
      changeValues(['.star_FeH'],'input[name=star1_FeH]');
    });
</script>
C;

//////////////////////////////////////////////////////////////////////////////////
//MODES
//////////////////////////////////////////////////////////////////////////////////

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//CATALOGUE MODE
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(preg_match("/Catalogue/",$Modes)){

  $TABID=1;

  //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  //CATALOGUE KEYS
  //$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  $keys=file($SESSDIR."/BHMcat.keys");
  $catfields="";
  foreach($keys as $key){
    $key=rtrim($key);
    $catfields.="<option value='$key'>$key</option>";
  }

$tabs.=<<<C
  $ajax_cat_Load
  <!-- //////////////////////////////////////////////////////////// -->
  <!-- CATALOGUE -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="Introduction" title="BHM Catalogue">
    <p><b>Binary Habitability Catalogue</b></p>
    <form id="cat_form" action="BHMcat.php">
      <input type="hidden" name="catid" value="$SESSID">
      Sort field:
      <select name="sortfield">
	$catfields
      </select>
      Sort order:
      <select name="sortorder">
	<option value="0">Ascending</option>
	<option value="1">Descending</option>
      </select>
      Detail level:
      <select name="displaylevel">
	<option value="1">Basic Properties</option>
	<option value="2">Detailed</option>
	<option value="3">All properties</option>
	<option value="4">All properties and errors</option>
      </select>
      Filter : <input type="text" name="catfilter" value="binary_Pbin>0">
      <a href="JavaScript:void(0)" style="font-size:10px" onclick="$('.help').toggle('fast',null)">Show/Hide Help</a>
      <div class="help" style="display:none">
	<b>Filter examples</b>:<br/>
	Periods in a given range: binary_Pbin>10 and binary_Pbin<40<br/>
	Primary stars with measured rotational velocity: star1_Protv>0<br/>
	Both stars with measured rotational velocity: star1_Protv>0 and star2_Protv<br/>
	Kepler planets: 'Kepler' in PlanetID<br/>
	Systems in DEBCat: 'DEB' in SourceCat<br/>
	Systems in Ekar catalogue with measured distance: 'Ek' in SourceCat and binary_d>0<br/>
      </div>
      <p></p>
      <button class="update" id="cat_Update">Update</button> 
      $ajaxform_cat_Update
      $force_update
      <div id="cat_results_panel" class="catalogue">
	<div class="download" id="cat_download"></div>
	<div id="cat_results_status_loader" style="background-color:white;">
	  <div id="cat_results_status" style="background-color:white;">
	    <iframe class="iframe" id="cat_results_frame" src="web/blank.html" 
		    scrolling="yes" onload="adjustiFrame(this);">
	    </iframe>
	  </div>
	</div>
      </div>
    </form>
  </div>
C;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//STAR MODE
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(preg_match("/Star1/",$Modes)){
  $TABID=1;
  $QCALCMODE=1;

  $star1_str_model_sel=selectFunction("star1_str_model",$MODELS,$star1_str_model,
				      $options="class='sensitive' onchange='idSystem();'");

  $star1_str_rotmodel_sel=selectFunction("star1_str_rotmodel",$ROTMODELS,$star1_str_rotmodel,
					 $options="class='sensitive' onchange='idSystem();'");

  if($Modes!="Star1"){$NumStar="1";}
  else{$NumStar="";}
$tabs.=<<<F
  <!-- //////////////////////////////////////////////////////////// -->
  <!-- STAR 1 -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="star1" title="Star $NumStar">
    <form id="star1_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="star">
	    <input type="hidden" name="object" value="star1">
	    <table border=0px>
	      <!-- ====================== BASIC =========================== -->
	      <tr><td colspan=2 class="section">Basic Properties</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Star ID:</td>
		<td class="field">
		  <input type="text" name="star1_str_StarID" value="$star1_str_StarID" >
		</td>
	      </tr>
	      <tr><td class="help" colspan=2>Apostrophes are mandatory, e.g. 'Star 1'</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Mass:</td>
		<td class="field">
		  <input class="sensitive" type="text" name="star1_M" value="$star1_M" onchange="changePlanetMorb();idSystem();">
		  M<sub>Sun</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Maximum recommended mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Metals content, Z:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="star1_Z" value="$star1_Z">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Fraction of mass in metals.  Z = 0.015 for the Sun.
		  Leave 0 to scale it from Y value and [Fe/H]
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Helium content, Y:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="star1_Y" value="$star1_Y">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Fraction of mass in Helium.  For the Sun Y = 0.276.  It never could be 0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Fraction of Fe, A:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="star1_A" value="$star1_A">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Fe fraction of metals.  A = 1.0 for pure Iron.
		  Valid range A = 0.9-1.0.  Typical, A = 0.95.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Metallicity, [Fe/H]:</td>
		<td class="field">
		  <input type="text" class="star_FeH sensitive" name="star1_FeH" value="$star1_FeH">
		  dex
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Observed metallicity.  For the Sun [Fe/H] = 0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Age:</td>
		<td class="field">
		  <input id="ini" type="text" class="star_tau sensitive" name="star1_tau" value="$star1_tau" onchange="changeValues(['.star_tau'],this);idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Estimated age of the star.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Main Sequence:</td>
		<td class="field">
		  <input class="sensistive" type="text" id="test" name="star1_taums" value="$star1_taums" onchange="idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Main sequence time.  Leave zero if you expect that
		  the tool calculate it by itself.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Stellar Model:</td>
		<td class="field">
		  $star1_str_model_sel
		  <!--<input class="sensistive" type="text" id="test" name="star1_str_model" value="$star1_str_model" onchange="idSystem();">-->
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar evolution model.  Available: BCA98, PARSEC, YZVAR, BASTI.
		</td>
	      </tr>

	      <!-- ====================== ROTATIONAL EVOLUTION =========================== -->
	      <tr><td colspan=2 class="section">Rotational Evolution</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Rotation Model:</td>
		<td class="field">$star1_str_rotmodel_sel</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Rotational Evolution model
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Disk age:</td><td class="field"><input type="text" name="star1_taudisk" value="$star1_taudisk"> Gyr</td></tr>
	      <tr><td class="help" colspan=2>Age of the circumstellar disk.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Initial period:</td><td class="field"><input type="text" name="star1_Pini" value="$star1_Pini"> days</td></tr>
	      <tr><td class="help" colspan=2>Initial rotational period.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Saturation period:</td><td class="field"><input type="text" name="star1_wsat" value="$star1_wsat"> &Omega;<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Leave it zero to scale with convective overturn time (see Gallet & Bouvier (2013).</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">AM transport timescale:</td><td class="field"><input type="text" name="star1_tauc" value="$star1_tauc"> Myr</td></tr>
	      <tr><td class="help" colspan=2>Typical timescale for AM transport inside star.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Wind torque scaling, K<sub>W</sub>:</td><td class="field"><input type="text" name="star1_Kw" value="$star1_Kw"></td></tr>
	      <tr><td class="help" colspan=2>Constant in Kawaler model.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">ML/Wind torque scaling, K<sub>C</sub>:</td><td class="field"><input type="text" name="star1_Kc" value="$star1_Kc"></td></tr>
	      <tr><td class="help" colspan=2>Constant in Chaboyer model.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Alfven radius scaling, K<sub>1</sub>:</td><td class="field"><input type="text" name="star1_K1" value="$star1_K1"></td></tr>
	      <tr><td class="help" colspan=2>Constant in Matt model.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Dynamo exponent, a:</td><td class="field"><input type="text" name="star1_a" value="$star1_a"></td></tr>
	      <tr><td class="help" colspan=2>Exponent of magnetic field scaling with rotation.  Normally a = 1.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Field geometry exponent, n:</td><td class="field"><input type="text" name="star1_n" value="$star1_n"></td></tr>
	      <tr><td class="help" colspan=2>Exponent of field geometry decay, n = 3/7 for dipolar field.  Normally n is taken as 1.5.</td></tr>

	      <!-- ====================== OBSERVED =========================== -->
	      <tr><td colspan=2 class="section">Observed Properties</td></tr>
	      <div style="display:none">
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Mass (error):</td><td class="field"><input type="text" name="star1_Merr" value="$star1_Merr"> M<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Period (velocity):</td><td class="field"><input type="text" name="star1_Protv" value="$star1_Protv"> days</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Period (velocity,error):</td><td class="field"><input type="text" name="star1_Protverr" value="$star1_Protverr"> days</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Period (photometry):</td><td class="field"><input type="text" name="star1_Prot" value="$star1_Prot"> days</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Period (photometry,error):</td><td class="field"><input type="text" name="star1_Proterr" value="$star1_Proterr"> days</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Radius:</td><td class="field"><input type="text" name="star1_R" value="$star1_R"> R<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Radius (error):</td><td class="field"><input type="text" name="star1_Rerr" value="$star1_Rerr"> R<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Effective Temperature:</td><td class="field"><input type="text" name="star1_T" value="$star1_T"> K</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Effective Temperature (error):</td><td class="field"><input type="text" name="star1_Terr" value="$star1_Terr"> K</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Surface Gravity:</td><td class="field"><input type="text" name="star1_logg" value="$star1_logg"> dex (cm s<sup>-2</sup>)</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Surface Gravity (error):</td><td class="field"><input type="text" name="star1_loggerr" value="$star1_loggerr"> dex (cm s<sup>-2</sup>)</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>

	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name" valign="top">
		  <a class="activelink" 
		     href="JavaScript:loadAjax('BHMutil.php?ACTION=SaveObject&ObjType=Star&NewId='+$('#saveobject_star1').val(),'#saveobjectdisp_star1');">
		  Save this object:
		  </a>
		</td>
		<td class="field">
		  <input id="saveobject_star1" type="text" name="saveobject" value="$binary_str_SysID-star1"><br/>
		  <div class="target" id="saveobjectdisp_star1"></div>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Pressing the link you will save the object with the name provided in the text box.
		</td>
	      </tr>

	      <!-- ====================== HIDDEN =========================== -->
	      <input type="hidden" name="star1_str_Stype" value="$star1_str_Stype">
	      <input type="hidden" name="star1_vsini" value="$star1_vsini">
	      <input type="hidden" name="star1_vsinierr" value="$star1_vsinierr">

	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="star1_Update">Update</button>
		  $ajaxform_star1_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="star1_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>

	  <div class="stdout" id="star1_stdout">
	    <a href="tmp/BHMrun-stdout-$SESSID-star" target="_blank">
	      stdout
	    </a> | 
	    <a href="tmp/BHMrun-stderr-$SESSID-star" target="_blank">
	      stderr
	    </a>
	  </div>

	  <div class="download" id="star1_download"></div>
	  <div id="star1_results_status_loader" style="background-color:white;">
	    <div id="star1_results_status" style="background-color:white;">
	      <iframe class="iframe" id="star1_results_frame" src="web/blank.html"
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   </form>
  </div>
F;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//BINARY MODE
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(preg_match("/Star2/",$Modes)){
  $TABID=3;
  $QCALCMODE=1;

  $star2_str_model_sel=selectFunction("star2_str_model",$MODELS,$star2_str_model,
				      $options="class='sensitive' onchange='idSystem();'");


  $star2_str_rotmodel_sel=selectFunction("star2_str_rotmodel",$ROTMODELS,$star2_str_rotmodel,
					 $options="class='sensitive' onchange='idSystem();'");

$tabs.=<<<F
  <!-- //////////////////////////////////////////////////////////// -->
  <!-- STAR 2 -->
  <!-- //////////////////////////////////////////////////////////// -->
  <div class="tabbertab" id="star2" title="Star 2">
    <form id="star2_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="star">
	    <input type="hidden" name="object" value="star2">
	    <table border=0px>
	      <!-- ====================== BASIC =========================== -->
	      <tr><td colspan=2 class="section">Basic Properties</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Star ID:</td>
		<td class="field">
		  <input type="text" name="star2_str_StarID" value="$star2_str_StarID" >
		</td>
	      </tr>
	      <tr><td class="help" colspan=2>Apostrophes are mandatory, e.g. 'Star 1'</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Mass:</td>
		<td class="field">
		  <input class="sensitive" type="text" name="star2_M" value="$star2_M" onchange="changePlanetMorb();idSystem();">
		  M<sub>Sun</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar mass.  Maximum recommended mass 1.5 M<sub>sun</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Metals content, Z:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="star2_Z" value="$star2_Z">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Fraction of mass in metals.  Z = 0.015 for the Sun.
		  Leave 0 to scale it from Y value and [Fe/H]
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Helium content, Y:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="star2_Y" value="$star2_Y">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Fraction of mass in Helium.  For the Sun Y = 0.276.  It never could be 0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Fraction of Fe, A:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="star2_A" value="$star2_A">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Fe fraction of metals.  A = 1.0 for pure Iron.
		  Valid range A = 0.9-1.0.  Typical, A = 0.95.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Metallicity, [Fe/H]:</td>
		<td class="field">
		  <input type="text" class="star_FeH sensitive" name="star2_FeH" value="$star2_FeH">
		  dex
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Observed metallicity.  For the Sun [Fe/H] = 0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Age:</td>
		<td class="field">
		  <input id="ini" type="text" class="star_tau sensitive" name="star2_tau" value="$star2_tau" onchange="changeValues(['.star_tau'],this);idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Estimated age of the star.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Main Sequence:</td>
		<td class="field">
		  <input class="sensistive" type="text" id="test" name="star2_taums" value="$star2_taums" onchange="idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Main sequence time.  Leave zero if you expect that
		  the tool calculate it by itself.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Stellar Model:</td>
		<td class="field">
		  $star2_str_model_sel
		  <!--<input class="sensistive" type="text" id="test" name="star2_str_model" value="$star2_str_model" onchange="idSystem();">-->
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Stellar evolution model.  Available: BCA98, PARSEC, YZVAR, BASTI.
		</td>
	      </tr>

	      <!-- ====================== ROTATIONAL EVOLUTION =========================== -->
	      <tr><td colspan=2 class="section">Rotational Evolution</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Rotation Model:</td>
		<td class="field">$star2_str_rotmodel_sel</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Rotational Evolution model
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Disk age:</td><td class="field"><input type="text" name="star2_taudisk" value="$star2_taudisk"> Gyr</td></tr>
	      <tr><td class="help" colspan=2>Age of the circumstellar disk.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Initial period:</td><td class="field"><input type="text" name="star2_Pini" value="$star2_Pini"> days</td></tr>
	      <tr><td class="help" colspan=2>Initial rotational period.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Saturation period:</td><td class="field"><input type="text" name="star2_wsat" value="$star2_wsat"> &Omega;<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Leave it zero to scale with convective overturn time (see Gallet & Bouvier (2013).</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">AM transport timescale:</td><td class="field"><input type="text" name="star2_tauc" value="$star2_tauc"> Myr</td></tr>
	      <tr><td class="help" colspan=2>Typical timescale for AM transport inside star.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Wind torque scaling, K<sub>W</sub>:</td><td class="field"><input type="text" name="star2_Kw" value="$star2_Kw"></td></tr>
	      <tr><td class="help" colspan=2>Constant in Chaboyer model.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">ML/Wind torque scaling, K<sub>C</sub>:</td><td class="field"><input type="text" name="star2_Kc" value="$star2_Kc"></td></tr>
	      <tr><td class="help" colspan=2>Constant in Chaboyer model.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Alfven radius scaling, K<sub>1</sub>:</td><td class="field"><input type="text" name="star2_K1" value="$star2_K1"></td></tr>
	      <tr><td class="help" colspan=2>Constant in Matt model.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Dynamo exponent, a:</td><td class="field"><input type="text" name="star2_a" value="$star2_a"></td></tr>
	      <tr><td class="help" colspan=2>Exponent of magnetic field scaling with rotation.  Normally a = 1.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Field geometry exponent, n:</td><td class="field"><input type="text" name="star2_n" value="$star2_n"></td></tr>
	      <tr><td class="help" colspan=2>Exponent of field geometry decay, n = 3/7 for dipolar field.  Normally n is taken as 1.5.</td></tr>

	      <!-- ====================== OBSERVED =========================== -->
	      <tr><td colspan=2 class="section">Observed Properties</td></tr>
	      <div style="display:none">
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Mass (error):</td><td class="field"><input type="text" name="star2_Merr" value="$star2_Merr"> M<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Period (velocity):</td><td class="field"><input type="text" name="star2_Protv" value="$star2_Protv"> days</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Period (velocity,error):</td><td class="field"><input type="text" name="star2_Protverr" value="$star2_Protverr"> days</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Period (photometry):</td><td class="field"><input type="text" name="star2_Prot" value="$star2_Prot"> days</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Period (photometry,error):</td><td class="field"><input type="text" name="star2_Proterr" value="$star2_Proterr"> days</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Radius:</td><td class="field"><input type="text" name="star2_R" value="$star2_R"> R<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Radius (error):</td><td class="field"><input type="text" name="star2_Rerr" value="$star2_Rerr"> R<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Effective Temperature:</td><td class="field"><input type="text" name="star2_T" value="$star2_T"> K</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Effective Temperature (error):</td><td class="field"><input type="text" name="star2_Terr" value="$star2_Terr"> K</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Surface Gravity:</td><td class="field"><input type="text" name="star2_logg" value="$star2_logg"> dex (cm s<sup>-2</sup>)</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Surface Gravity (error):</td><td class="field"><input type="text" name="star2_loggerr" value="$star2_loggerr"> dex (cm s<sup>-2</sup>)</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name" valign="top">
		  <a class="activelink" 
		     href="JavaScript:loadAjax('BHMutil.php?ACTION=SaveObject&ObjType=Star&NewId='+$('#saveobject_star2').val(),'#saveobjectdisp_star2');">
		  Save this object:
		  </a>
		</td>
		<td class="field">
		  <input id="saveobject_star2" type="text" name="saveobject" value="$binary_str_SysID-star2"><br/>
		  <div class="target" id="saveobjectdisp_star2"></div>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Pressing the link you will save the object with the name provided in the text box.
		</td>
	      </tr>

	      <!-- ====================== HIDDEN =========================== -->
	      <input type="hidden" name="star2_str_Stype" value="$star2_str_Stype">
	      <input type="hidden" name="star2_vsini" value="$star2_vsini">
	      <input type="hidden" name="star2_vsinierr" value="$star2_vsinierr">

	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="star2_Update">Update</button>
		  $ajaxform_star2_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="star2_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>

	  <div class="stdout" id="star2_stdout">
	    <a href="tmp/BHMrun-stdout-$SESSID-star" target="_blank">
	      stdout
	    </a> | 
	    <a href="tmp/BHMrun-stderr-$SESSID-star" target="_blank">
	      stderr
	    </a>
	  </div>

	  <div class="download" id="star2_download"></div>
	  <div id="star2_results_status_loader" style="background-color:white;">
	    <div id="star2_results_status" style="background-color:white;">
	      <iframe class="iframe" id="star2_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   </form>
  </div>
F;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//PLANET MODE
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(preg_match("/Planet/",$Modes)){
  $TABID=1;
  $QCALCMODE=1;

$tabs.=<<<F
  <div class="tabbertab" id="planet" title="Planet">
  <form id="planet_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="planet_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="planet">
	    <input type="hidden" name="object" value="planet">
	    <table border=0px>
	      <!-- ====================== OBSERVED =========================== -->
	      <tr><td colspan=2 class="section">Basic Properties</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Planet ID:</td>
		<td class="field">
		  <input type="text" name="planet_str_PlanetID" value="$planet_str_PlanetID" >
		</td>
	      </tr>
	      <tr><td class="help" colspan=2></td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Mass:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="planet_M" value="$planet_M" onchange="idSystem();">
		  M<sub>Earth</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Minimum mass 1.0, maximum mass 320 M<sub>Earth</sub>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">H/He Mass Fraction:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="planet_fHHe" value="$planet_fHHe" onchange="idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Smaller than 1.  Not important for Earth-like planets.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Core Mass Fraction:</td>
		<td class="field">
		  <input type="text" class="sensitive" name="planet_CMF" value="$planet_CMF" onchange="idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Smaller than 1.  Earth is CMF=0.34
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Planetary Age:</td>
		<td class="field">
		  <input type="text" class="star_tau sensitive" name="planet_tau" value="$planet_tau" onchange="changeValues(['.star_tau'],this);idSystem();">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Planetary Age.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Orbiting Mass:</td>
		<td class="field">
		  <input type="text" id="planet_Morb" class="sensistive" name="planet_Morb" value="$planet_Morb" onchange="idSystem();">
		  M<sub>Sun</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  In case of a binary this should be the sum of M1 + M2.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Orbital semimajor axis:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="planet_aorb" value="$planet_aorb" onchange="idSystem();">
		  AU
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Larger than stellar radius.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Orbital period:</td>
		<td class="field">
		  <input type="text" id="test" class="sensistive" name="planet_Porb" value="$planet_Porb" onchange="idSystem();">
		  days
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Leave blank for calculation
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Orbital eccentricity:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="planet_eorb" value="$planet_eorb" onchange="idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  0&lt;e&lt;1
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Argument of periapsis:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="planet_worb" value="$planet_worb" onchange="idSystem();">
		  degrees
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  0<&omega;<360<sup>o</sup>
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Rotational Period:</td>
		<td class="field">
		  <input type="text" id="test" class="sensitive" name="planet_Prot" value="$planet_Prot" onchange="idSystem();">
		  days
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Not larger than orbital period
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="planet_Update">Update</button> 
		  $ajaxform_planet_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ====================== OBSERVED =========================== -->
	      <tr><td colspan=2 class="section">Observed Properties</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Radius:</td><td class="field"><input type="text" name="planet_R" value="$planet_R"> R<sub>Earth</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>

	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name" valign="top">
		  <a class="activelink" 
		     href="JavaScript:loadAjax('BHMutil.php?ACTION=SaveObject&ObjType=Planet&NewId='+$('#saveobject_planet').val(),'#saveobjectdisp_planet');">
		  Save this object:
		  </a>
		</td>
		<td class="field">
		  <input id="saveobject_planet" type="text" name="saveobject" value="$binary_str_SysID-planet"><br/>
		  <div class="target" id="saveobjectdisp_planet"></div>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Pressing the link you will save the object with the name provided in the text box.
		</td>
	      </tr>

	      <!-- ====================== HIDDEN =========================== -->
	      <input type="hidden" name="planet_Porberr" value="$planet_Porberr">
	      <input type="hidden" name="planet_aorberr" value="$planet_aorberr">
	      <input type="hidden" name="planet_eorberr" value="$planet_eorberr">
	      <input type="hidden" name="planet_worberr" value="$planet_worberr">
	      <input type="hidden" name="planet_Merr" value="$planet_Merr">
	      <input type="hidden" name="planet_Rerr" value="$planet_Rerr">

	    </table>
	</div>
	<div id="planet_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>

	  <div class="download" id="planet_download"></div>

	  <div class="stdout" id="planet_stdout">
	    <a href="tmp/BHMrun-stdout-$SESSID-planet" target="_blank">
	      stdout
	    </a> | 
	    <a href="tmp/BHMrun-stderr-$SESSID-planet" target="_blank">
	      stderr
	    </a>
	  </div>

	  <div id="planet_results_status_loader" style="background-color:white;">
	    <div id="planet_results_status" style="background-color:white;">
	      <iframe class="iframe" id="planet_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   </form>
  </div>
F;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//BINARY
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(preg_match("/Binary/",$Modes)){
  $TABID=4;
  $QCALCMODE=1;

$tabs.=<<<F
  <div class="tabbertab" id="binary" title="Binary">
  <form id="binary_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="binary_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="binary">
	    <input type="hidden" name="object" value="binary">
	    <table border=0px>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">System ID:</td>
		<td class="field">
		  <input type="text" name="binary_str_SysID" value="$binary_str_SysID" >
		</td>
	      </tr>
	      <tr><td class="help" colspan=2></td></tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Binary period:</td>
		<td class="field">
		  <input class="sensitive" type="text" name="binary_Pbin" value="$binary_Pbin" onchange="idSystem();">
		  days
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Longer than 0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Binary semimajor axis:</td>
		<td class="field">
		  <input  class="sensitive" type="text" name="binary_abin" value="$binary_abin" onchange="idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Larger than 0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Binary Eccentricity:</td>
		<td class="field">
		  <input class="sensitive" type="text" name="binary_ebin" value="$binary_ebin" onchange="idSystem();">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  0&lt;e&gt;1
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Binary Argument of Periastron:</td>
		<td class="field">
		  <input type="text" name="binary_wbin" value="$binary_wbin"> deg
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2></td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Binary Inclination:</td>
		<td class="field">
		  <input type="text" name="binary_ibin" value="$binary_ibin"> deg
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2></td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="binary_Update">Update</button> 
		  $ajaxform_binary_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <!-- ====================== OBSERVED =========================== -->
	      <tr><td colspan=2 class="section">Observed Properties</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Visual Magnitude:</td><td class="field"><input type="text" name="binary_V" value="$binary_V"> mag</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Color Index, B-V:</td><td class="field"><input type="text" name="binary_BV" value="$binary_BV"> mag</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Distance (photometric):</td><td class="field"><input type="text" name="binary_dmod" value="$binary_dmod"> pc</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Distance (parallax):</td><td class="field"><input type="text" name="binary_d" value="$binary_d"> pc</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Distance (parallax, error):</td><td class="field"><input type="text" name="binary_derr" value="$binary_derr"> pc</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Minimum age:</td><td class="field"><input type="text" name="binary_taumin" value="$binary_taumin"> Gyr</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">Maximum age:</td><td class="field"><input type="text" name="binary_taumax" value="$binary_taumax"> Gyr</td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>
	      <!-- ---------------------------------------- -->
	      <tr><td class="name">X-Ray Luminosity:</td><td class="field"><input type="text" name="binary_Lx" value="$binary_Lx"> L<sub>Sun</sub></td></tr>
	      <tr><td class="help" colspan=2>Help.</td></tr>

	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name" valign="top">
		  <a class="activelink" 
		     href="JavaScript:loadAjax('BHMutil.php?ACTION=SaveObject&ObjType=Binary&NewId='+$('#saveobject_binary').val(),'#saveobjectdisp_binary');">
		  Save this object:
		  </a>
		</td>
		<td class="field">
		  <input id="saveobject_binary" type="text" name="saveobject" value="$binary_str_SysID-binary"><br/>
		  <div class="target" id="saveobjectdisp_binary"></div>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Pressing the link you will save the object with the name provided in the text box.
		</td>
	      </tr>

	      <!-- ====================== HIDDEN =========================== -->
	      <input type="hidden" name="binary_Zfit" value="$binary_Zfit">
	      <input type="hidden" name="binary_FeHfit" value="$binary_FeHfit">
	      <input type="hidden" name="binary_FeHfiterr" value="$binary_FeHfiterr">
	      <input type="hidden" name="binary_Zobs" value="$binary_Zobs">
	      <input type="hidden" name="binary_FeHobs" value="$binary_FeHobs">
	      <input type="hidden" name="binary_q" value="$binary_q">
	      <!-- ---------------------------------------- -->

	    </table>
	</div>
	<div id="binary_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>

	  <div class="download" id="binary_download"></div>

	  <div class="stdout" id="binary_stdout">
	    <a href="tmp/BHMrun-stdout-$SESSID-binary" target="_blank">
	      stdout
	    </a> | 
	    <a href="tmp/BHMrun-stderr-$SESSID-binary" target="_blank">
	      stderr
	    </a>
	  </div>

	  <div id="binary_results_status_loader" style="background-color:white;">
	    <div id="binary_results_status" style="background-color:white;">
	      <iframe class="iframe" id="binary_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   <input class="sys_input" type="hidden" name="binary_str_sys" value="$binary_str_sys">
   </form>
  </div>
F;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//HABITABILITY
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(preg_match("/Habitability/",$Modes)){
  $TABID=5;
  $QCALCMODE=1;

  $hz_str_incrit_wd_sel=selectFunction("hz_str_incrit_wd",$HZINMODELS,$hz_str_incrit_wd,
				       $options="");
  $hz_str_incrit_nr_sel=selectFunction("hz_str_incrit_nr",$HZINMODELS,$hz_str_incrit_nr,
				       $options="");
  $hz_str_outcrit_wd_sel=selectFunction("hz_str_outcrit_wd",$HZOUTMODELS,$hz_str_outcrit_wd,
					$options="");
  $hz_str_outcrit_nr_sel=selectFunction("hz_str_outcrit_nr",$HZOUTMODELS,$hz_str_outcrit_nr,
					$options="");
$tabs.=<<<F
  <div class="tabbertab" id="hz" title="Habitable Zone">
  <form id="hz_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="hz_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="hz">
	    <input type="hidden" name="object" value="hz">
	    <table border=0px>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">Inner edge (wider HZ):</td>
		<td class="field">
		  $hz_str_incrit_wd_sel
		  <!--<input type="text" name="hz_str_incrit_wd" value="$hz_str_incrit_wd">-->
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'recent venus', 'moist greenhouse',
		  'runaway greenhouse' (sustained lowercase)
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
		<td class="name">Outer edge (wider HZ):</td>
		<td class="field">
		  $hz_str_outcrit_wd_sel
		  <!--<input type="text" name="hz_str_outcrit_wd" value="$hz_str_outcrit_wd">-->
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'maximum greenhouse', 'early mars' (sustained lowercase)
		</td>
	      </tr>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">Inner edge (conservative HZ):</td>
		<td class="field">
		  $hz_str_incrit_nr_sel
		  <!--<input type="text" name="hz_str_incrit_nr" value="$hz_str_incrit_nr">-->
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'recent venus', 'moist greenhouse',
		  'runaway greenhouse' (sustained lowercase)
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Outer edge (conservative HZ):</td>
		<td class="field">
		  $hz_str_outcrit_nr_sel
		  <!--<input type="text" name="hz_str_outcrit_nr" value="$hz_str_outcrit_nr">-->
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'maximum greenhouse', 'early mars' (sustained lowercase)
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name" valign="top">
		  <a class="activelink" 
		     href="JavaScript:loadAjax('BHMutil.php?ACTION=SaveObject&ObjType=HZ&NewId='+$('#saveobject_hz').val(),'#saveobjectdisp_hz');">
		  Save this object:
		  </a>
		</td>
		<td class="field">
		  <input id="saveobject_hz" type="text" name="saveobject" value="$binary_str_SysID-hz"><br/>
		  <div class="target" id="saveobjectdisp_hz"></div>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Pressing the link you will save the object with the name provided in the text box.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="hz_Update">Update</button> 
		  $ajaxform_hz_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="hz_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>

	  <div class="download" id="hz_download"></div>

	  <div class="stdout" id="hz_stdout">
	    <a href="tmp/BHMrun-stdout-$SESSID-hz" target="_blank">
	      stdout
	    </a> | 
	    <a href="tmp/BHMrun-stderr-$SESSID-hz" target="_blank">
	      stderr
	    </a>
	  </div>

	  <div id="hz_results_status_loader" style="background-color:white;">
	    <div id="hz_results_status" style="background-color:white;">
	      <iframe class="iframe" id="hz_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   <input class="sys_input" type="hidden" name="hz_str_sys" value="$hz_str_sys">
   </form>
  </div>
F;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//INTERACTION
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(preg_match("/Interactions/",$Modes)){
  $TABID=7;
  $QCALCMODE=1;

$updateall=<<<F
$ajax_all_Update
<div style="position:fixed;top:10px;right:10px">
<form id="allforms" action="JavaScript:void(0)">
  <button id="all_Update">Update All</button>
  $ajax_all_Update
</form>
</div>
F;

$tabs.=<<<F
  $ajax_all_Update	    
  <div class="tabbertab" id="rotation" title="Rotation and Activity">
  <form id="rotation_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="rotation_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="rotation">
	    <input type="hidden" name="object" value="rotation">
	    <table border=0px>
	      <tr>
		<!-- ---------------------------------------- -->
		<td class="name">&tau;<sub>int</sub>:</td>
		<td class="field">
		  <input type="text" name="rotation_tauint" value="$rotation_tauint"> Myr
		</td> 
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Common time-scale of interaction among binaries or
		  with a common accretion disk.
		</td>
	      </tr>
		<!-- ---------------------------------------- -->
		<td class="name">f<sub>diss</sub>:</td>
		<td class="field">
		  <input type="text" name="rotation_fdiss" value="$rotation_fdiss">
		</td> 
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Fraction of convective turnover time required for
		  tidal dissipation.  Usually
		  f<sub>diss</sub>=1.0-3.5.
		</td>
	      </tr>

	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name" valign="top">
		  <a class="activelink" 
		     href="JavaScript:loadAjax('BHMutil.php?ACTION=SaveObject&ObjType=Rotation&NewId='+$('#saveobject_rot').val(),'#saveobjectdisp_rot');">
		  Save this object:
		  </a>
		</td>
		<td class="field">
		  <input id="saveobject_rot" type="text" name="saveobject" value="$binary_str_SysID-rot"><br/>
		  <div class="target" id="saveobjectdisp_rot"></div>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Pressing the link you will save the object with the name provided in the text box.
		</td>
	      </tr>

	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="rotation_Update">Update</button> 
		  $ajaxform_rotation_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="rotation_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>

	  <div class="download" id="rotation_download"></div>

	  <div class="stdout" id="rotation_stdout">
	    <a href="tmp/BHMrun-stdout-$SESSID-rotation" target="_blank">
	      stdout
	    </a> | 
	    <a href="tmp/BHMrun-stderr-$SESSID-rotation" target="_blank">
	      stderr
	    </a>
	  </div>

	  <div id="rotation_results_status_loader" style="background-color:white;">
	    <div id="rotation_results_status" style="background-color:white;">
	      <iframe class="iframe" id="rotation_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
   <input class="sys_input" type="hidden" name="rotation_str_sys" value="$rotation_str_sys">
   </form>
  </div>
F;

$interaction_str_refobj_sel=selectFunction("interaction_str_refobj",$REFOBJS,
					   $interaction_str_refobj,
					   $options="");
$tabs.=<<<F
  <div class="tabbertab" id="summary" title="Binary-Planet Interaction">
  <form id="interaction_form" action="BHMrun.php">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="interaction_form" class="formarea">
	  <div><center class="title">Input Form</center><hr width="90%"/></div>
	    <input type="hidden" name="module" value="interaction">
	    <input type="hidden" name="object" value="interaction">
	    <table border=0px>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Initial time:</td>
		<td class="field">
		  <input type="text" name="interaction_tauini" value="$interaction_tauini">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Initial time for integration.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Reference time</td>
		<td class="field">
		  <input type="text" name="interaction_tauref" value="$interaction_tauref">
		  Gyr
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Reference time for mass-loss calculations.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Magnetosphere Reference Object:</td>
		<td class="field">
		  $interaction_str_refobj_sel		  
		  <!--<input type="text" name="interaction_str_refobj" value="$interaction_str_refobj">-->
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Available: 'Earth', 'Saturn'
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Standoff distance, M-exponent:</td>
		<td class="field">
		  <input type="text" name="interaction_nM" value="$interaction_nM">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  For most magnetospheres n<sub>M</sub>=3.0.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Standoff distance, P-exponent:</td>
		<td class="field">
		  <input type="text" name="interaction_nP" value="$interaction_nP">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  For stiff magnetospheres (Earth-like to
		  Neptune-like) n<sub>P</sub>=6.0, for responsive
		  magnetospheres (gas giants) n<sub>P</sub>=4.5.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Entrapment factor</td>
		<td class="field">
		  <input type="text" name="interaction_alpha" value="$interaction_alpha">
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  For Venus &alpha;=0.3 fits well early mass-loss.
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Atmospheric mean molecular weight</td>
		<td class="field">
		  <input type="text" name="interaction_muatm" value="$interaction_muatm">
		  g/mol
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Earth's atmosphere, &mu;<sub>atm</sub>=44 g/mol
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Minimum planetary mass for Mass-loss scaling</td>
		<td class="field">
		  <input type="text" name="interaction_Mmin" value="$interaction_Mmin">
		  M<sub>Earth</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Earth's atmosphere, &mu;<sub>atm</sub>=44 g/mol
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name">Maximum planetary mass for Mass-loss scaling</td>
		<td class="field">
		  <input type="text" name="interaction_Mmax" value="$interaction_Mmax">
		  M<sub>Earth</sub>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Earth atmosphere, &mu;<sub>atm</sub>=44 g/mol
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="name" valign="top">
		  <a class="activelink" 
		     href="JavaScript:loadAjax('BHMutil.php?ACTION=SaveObject&ObjType=Interaction&NewId='+$('#saveobject_int').val(),'#saveobjectdisp_int');">
		  Save this object:
		  </a>
		</td>
		<td class="field">
		  <input id="saveobject_int" type="text" name="saveobject" value="$binary_str_SysID-int"><br/>
		  <div class="target" id="saveobjectdisp_int"></div>
		</td>
	      </tr>
	      <tr>
		<td class="help" colspan=2>
		  Pressing the link you will save the object with the name provided in the text box.
		</td>
	      </tr>

	      <!-- ---------------------------------------- -->
	      <tr>
		<td class="button" colspan=2>
		  <button class="update" id="interaction_Update">Update</button> 
		  $ajaxform_interaction_Update
		  $force_update
		</td>
	      </tr>
	      <!-- ---------------------------------------- -->
	    </table>
	</div>
	<div id="interaction_results_panel" class="results">
	  <div><center class="title">Results</center><hr width="90%"/></div>

	  <div class="download" id="interaction_download"></div>
	  <div class="stdout" id="interaction_stdout">
	    <a href="tmp/BHMrun-stdout-$SESSID-interaction" target="_blank">
	      stdout
	    </a> | 
	    <a href="tmp/BHMrun-stderr-$SESSID-interaction" target="_blank">
	      stderr
	    </a>
	  </div>

	  <div id="interaction_results_status_loader" style="background-color:white;">
	    <div id="interaction_results_status" style="background-color:white;">
	      <iframe class="iframe" id="interaction_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
    <input class="sys_input" type="hidden" name="interaction_str_sys" value="$interaction_str_sys">
   </form>
   <input class="sys_input" type="hidden" name="interaction_str_sys" value="$interaction_str_sys">
  </div>
F;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//BUG REPORT
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$parts=preg_split("/:/",$Modes);
$bug_mode=$parts[count($parts)-1];
$bug_report=<<<B
<div style="position:fixed;top:35px;right:0px">
  <div style="text-align:right;padding:10px;z-index:100">
    <a href="JavaScript:void(0)" style="font-size:10px;background:white;padding:10px;text-align:right;border:solid black 1px;" onclick="display('bug_box');">Bug Report</a>
  </div>
  <div id="bug_box" style="display:none;border:solid black 1px;padding:10px;background:white;width:500px;font-size:12px;z-index:100000">
    <h3>Bug Report</h3>
    <p>Thank you for your active involvement in the improvement of
    $BHMcalc.  Filling a bug report is simple.</p><p>Provide
    (optionally) your contact information below and a brief
    description of the bug.</p><p>When submiting your report we will
    attach information about the system you are presently running.
    You do not need to provide any detailed information about the
    system.</p>
    <form id="bug_form" action="BHMutil.php">
      <input type="hidden" name="datetime" value="$DATETIME">
      <input type="hidden" name="ACTION" value="BugReport">
      <input type="hidden" name="Modes" value="$Modes">
      E-mail (optional) : <input name="bug_email" value="bug@bhmcalc.net"><br/>
      Report:<br/>
      <div id="bug_report" style="padding:10px;background:lightgray">
	<textarea rows="5" style="width:100%" name="bug_report">I have detected a problem with the calculator when running the tool in the '$bug_mode' mode. See details below.</textarea>
      </div>
      <div id="bug_result" style="padding:10px">Status: <i>Not sent</i></div>
      <button id="bug_send">Report</button>
      $ajax_bug
      <a href="JavaScript:void(0)" style="font-size:10px;float:right" onclick="display('bug_box')">Hide</a>
    </form>
  </div>
</div>
B;

if($QCALCMODE){
$cfile="$SESSDIR/configurations.html";
$ofile="$SESSDIR/objects.html";
if(is_file($ofile)){
  $objects=shell_exec("cat $ofile");
}else{
  $objects="<i>No objects saved yet.</i>";
}
if(is_file($cfile)){
  $configurations=shell_exec("cat $cfile");
  $downlink=<<<D
<a href="$wSESSDIR/configurations.html" target="_blank" style="font-size:10px">
  Download Configuration
</a>
D;
}else{$configurations="";$downlink="";}
$summary=<<<F
  $ajax_summary_Load
  <div class="tabbertab" id="summary" title="Summary">
    <form id="summary_form" action="BHMsummary.php">
    <input type="hidden" name="Mode" value="$oModes">
    <div class="tabcontent">
      <div class="wrapper">
	<div id="summary_form" class="formarea">
	  <div><center class="title">Additional Information</center><hr width="90%"/></div>
	  <button class="update" id="summary_Update">Update</button> 
	  $ajaxform_summary_Update
	  <ul>
	    <li class="summaryitem">
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=DownloadConfig&Modes=$oModes','#download_config');">
		Download configuration files.
	      </a>
	      <div class="target" id="download_config"></div>
	    </li>
	    <li class="summaryitem">
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=DownloadData&Modes=$oModes','#download_datafiles');">
		Download data files.
	      </a>
	      <div class="target" id="download_datafiles"></div>
	    </li>
	    <li class="summaryitem">
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=DownloadAll&Modes=$oModes','#download_allfiles');">
		Download all files.
	      </a>
	      <div class="target" id="download_allfiles"></div>
	    </li>
	    <li class="summaryitem">
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=MasterLink&Modes=$oModes','#systemlink');">
		Generate system link.</a>
	      <div class="target" id="systemlink"></div>
	    </li>
	    <li class="summaryitem">
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=CommandLine&Modes=$oModes','#commandline');">
		Generate command line.</a>
	      <div class="target" id="commandline"></div>
	    </li>
	    <li class="summaryitem">
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=SaveConfiguration&Modes=$oModes','#saveconfiguration');">
		Save Configuration</a> |
	      <a class="activelink" 
		 href="JavaScript:loadAjax('BHMutil.php?ACTION=CleanConfiguration&Modes=$oModes','#saveconfiguration');">
		Clear Configuration</a> 
	      <div class="listconfig" id="saveconfiguration"><ul>$configurations</ul></div>
	      $downlink
	    </li>
	    <li class="summaryitem">
	      Saved Objects:
	      <div class="listconfig" id="saveobjects">
		<ul>$objects</ul>
	      </div>
	    </li>
	  </ul>
	</div>
	<div id="summary_results_panel" class="results">
	  <div><center class="title">Summary of Results</center><hr width="90%"/></div>
	  <div class="download" id="summary_download"></div>
	  <div id="summary_results_status_loader" style="background-color:white;">
	    <div id="summary_results_status" style="background-color:white;">
	      <iframe id="summary_results_frame" src="web/blank.html" 
		      scrolling="yes" onload="adjustiFrame(this);">
	      </iframe>
	    </div>
	  </div>
	</div>
      </div>
    </div>
    </form>
  </div>
F;
$TABID=1;
}


//////////////////////////////////////////////////////////////////////////////////
//BASIC CONTENT
//////////////////////////////////////////////////////////////////////////////////
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//CHECK BORWSER
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$agent=$_SERVER["HTTP_USER_AGENT"];
$qchrome=0;
if(preg_match("/chrome/i",$agent)){$qchrome=1;}
if(!$qchrome){
$message=<<<MSG
<script>
$(document).ready(function(){
    setTimeout(function(){
	$('#message').fadeOut();
      },5000);
  });
</script>
<div id="message" style="background:pink;padding:10px;width:40%;font-size:12px;">
  This website is optimized to work with the Google Chrome web browser.
</div>
MSG;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//HEADER
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$header=mainHeader();
echo<<<HEAD
<html>
$header
<body>
  <!--MESSAGE AREA-->
  <div style="position:fixed;top:0px;width:100%;text-align:center;height:0px">
    <center>
      <div id="ad" style="display:$QMAINTAINANCE;background:lightyellow;padding:10px;width:30%;font-size:12px;font-style:italic;">
	<img src="web/maw.png" width=40px align="left"/>
	This site is under maintainance or it is being updated.
	Several functionalities could be temporarily out of order.
      </div>
      $message
    </center>
  </div>
  <!--BODY-->
     <div id="body" style="background-color:white;opacity:0.2;width:100%;height:100%">
    <center>
      <div id="rendering" style="z-index:10000;float:center;position:absolute;right:0px;border:solid black 0px;">
	<img src="web/load.gif">
      </div>
    </center>
HEAD;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//TRACKING
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
include_once("web/BHMtracking.php");

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//VERBOSE INFORMATION
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$CONTENT.="";
if($VERBOSE){
$CONTENT.=<<<C
Sessid:$SESSID<br/>
ROOTDIR: $ROOTDIR
GET: $GETSTR<br/>
POST: $POSTSTR<br/>
C;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//FRONTMATTER
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$CONTENT.=<<<C
<h1>
<a style='font-size:36' href="$wDIR/">
  BHM Calculator
</a><sup> <b style='color:red'>2.0</b><br/>
  <i style="font-size:18px">Binary Habitability and More</i></sup>
</h1>
C;

//////////////////////////////////////////////////////////////////////////////////
//CHOOSE CONTENT
//////////////////////////////////////////////////////////////////////////////////

//##############################
//INTRODUCTION
//##############################
include_once("web/main.php");

//##############################
//HELP
//##############################
include_once("web/help.php");
include_once("web/about.php");

//##############################
//FOOTER
//##############################
$footer=<<<C
<p></p>
<div class="footer">
  Developed by <a href="mailto:jorge.zuluaga@udea.edu.co">Jorge I. Zuluaga</a>
  <img src="web/copyleft.jpg" width=10px> 2014,
  Viva la BHM!, 
  Session ID: $SESSID.
  Server: $SERVER.
</div>
C;

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//UPDATE ALL
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
$udateall=<<<C
<div style="position:fixed;top:10px;right:10px">
<form id="allforms" action="JavaScript:void(0)">
  <button id="all_Update">Update All</button>
  $ajax_all_Update
</form>
</div>
C;

//////////////////////////////////////////////////////////////////////////////////
//HELP
//////////////////////////////////////////////////////////////////////////////////
if(isset($ABOUT)){$TABID=1;}
if(isset($HELP)){$TABID=2;}

//////////////////////////////////////////////////////////////////////////////////
//CREATE CONTENT
//////////////////////////////////////////////////////////////////////////////////
$CONTENT.=<<<C
<div class="tabber maintabber" name="tabber" id="$TABID">
  $bug_report
  $updateall
  $main
  $summary
  $tabs
  $about
  $help
</div>
$footer
C;

//////////////////////////////////////////////////////////////////////////////////
//CLOSING MATTER
//////////////////////////////////////////////////////////////////////////////////
$CONTENT.=<<<CONTENT
</div>
<br/>
<script>
  $(window).bind("load",function(){
  $("#body").css("opacity","1.0");
  $("#rendering").css("display","none");
  });
</script>
</body>
</html>
CONTENT;
echo $CONTENT;
?>
