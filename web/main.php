<?PHP
$main=<<<C
<div class="tabbertab" id="Introduction" title="Main">
  <div class="tabcontent">
    
    <p style="font-size:20px">
      Welcome to the <b>Binary Habitability (and More) Calculator</b>, $BHMcalc!
    </p>

    <p style="font-size:20px">What do you want to do?</p>

    <div style="text-align:center">
    <form action="$wDIR" method="post">
      <button class="mode" name="Modes" value="Introductory"><!-- style="border-color:black" -->
      Build your own system
      </button>
      <button class="mode" name="Modes" value="Random">
      Generate a Random System
      </button>
      <button class="mode" name="Modes" value="Catalogue">
      Choose a system from a catalogue
      </button>
    </form>
    </div>

    <p> 
      $BHMcalc is a web application intended to explore the vast
      configuration space of <b><i>Circumbinary Planetary System</i>
      </b> (aka. <a href="?HELP#Gallery"><i>Tatooines</i></a>).  
    </p>
    
    <p>
      You can use $BHMcalc to calculate the evolution of stars and
      planets in binaries and the complex interactions between them.
      These interations affect any potential <b>habitable environments
      around these systems</b>.
    </p>

    <p> If you want to use the calculator for more advanced purposes
    please select the
    <a href="?HELP#Modes">$BHMcalc Mode</a>: </p>

    <div style="text-align:center">
    <form action="$wDIR" method="post">
      <button class="mode" name="Modes" value="Star1">
	Star
      </button>
      <button class="mode" name="Modes" value="Planet">
	Planet
      </button>
      <button class="mode" name="Modes" value="Binary">
	Binary
      </button><br/>
      <button class="mode" name="Modes" value="Habitability">
	Habitability
      </button>
      <button class="mode" name="Modes" value="Interactions">
	Interactions
      </button>
    </form>
    </div>

    <!--
    <p> For <b>detailed instructions</b> or a description of the
      <b>functioning and science behind</b> $BHMcalc please refer to
      the <a href="?HELP">Help section</a>.  </p>
    -->
  </div>
</div>
C;
?>
