<?PHP
$main=<<<C
<div class="tabbertab" id="Introduction" title="Main">
  <div class="tabcontent">
    
    <p style="font-size:20px">
      Welcome to the <b>Binary Habitability (and More) Calculator</b>, $BHMcalc!
    </p>

    <p> 
      $BHMcalc is a web application intended to explore the vast
      configuration space of <b><i>Circumbinary Planetary System</i>
      </b> (aka. <a href="?HELP#Gallery"><i>Tatooines</i></a>).  You
      can use $BHMcalc to calculate the evolution of stars and planets
      in binaries and the complex interactions between them ultimately
      leading to (or limiting) the existence of <b>habitable
      environments around binaries</b>.
    </p>

    <p>
      Please select the <a href="?HELP#Modes">$BHMcalc Mode</a> you
      want to use:
    </p>

    <div style="text-align:center">
    <form action="$wDIR" method="post">
      <button class="mode" name="Modes" value="Intro" style="border-color:red">
      Basic
      </button><br/>
      <button class="mode" name="Modes" value="Catalogue">
	Catalogue
      </button>
      <button class="mode" name="Modes" value="Star1">
	Star
      </button>
      <button class="mode" name="Modes" value="Planet">
	Planet
      </button><br/>
      <button class="mode" name="Modes" value="Binary">
	Binary
      </button>
      <button class="mode" name="Modes" value="Habitability">
	Habitability
      </button>
      <button class="mode" name="Modes" value="Interactions">
	Interactions
      </button>
    </form>
    </div>

    <p>
      For a <b>quick start</b>, <b>detailed instructions</b> or a description of the
      <b>functioning and science behind</b> $BHMcalc please refer to
      the <a href="?HELP">Help section</a>.
    </p>

  </div>
</div>
C;
?>
