<?PHP
$main=<<<C
<div class="tabbertab" id="Introduction" title="Main">
  <div class="tabcontent">
    
    <p style="font-size:20px">
      Welcome to the <b>Binary Habitability Calculator</b>, $BHMcalc!
    </p>

    <p>
      $BHMcalc is a web application intended to explore the vast
      configuration space of <b><i>Circumbinary Planetary System</i>
      </b> (aka. <i>Tatooines</i>).  You can use it to calculate the
      evolution of stars in binaries, the changing properties of
      planets thriving around them and their interactions.
    </p>

    <p>
      Please select the <a href="?HELP#Modes">$BHMcalc Mode</a>:
    </p>

    <div style="text-align:center">
    <form action="$wDIR" method="post">
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

  </div>
</div>
C;
?>
