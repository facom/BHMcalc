<?PHP
$help=<<<C
<div class="tabbertab" id="Introduction" title="Help">
  <div class="tabcontent">

    <p class="title">Quick Start</p>

    <p>
     $BHMcalc works as a regular windows application. Its usage is
     intuitive and easy to master.
    </p>
    
    <p>
      The calculator could be used in different ways (<i>modes</i>):
      you can browse the <a href="?HELP#BHMcat">BHM catalogue</a>
      (Catalogue Mode), calculate the properties of a single star
      (Star Mode) or a planet (Planet Mode) or simply proceed to do
      the full thing (Interaction Mode), ie. calculate the property of
      stars in a binary system and their interaction with a planet.
    </p>
    <center>
      <div class="figure">
	<img src="doc/figures/modes.png" width="100%"/>
	<div class="caption">The Calculator Modes</div>
      </div>
    </center>
    
    <p>
      So, why don't you try the calculator while reading this
      guide.  <a href="?"  target="_blank">Click here</a> to open it
      in a new browser tab.
    </p>

    <a name="Modes"></a>
    <p class="subtitle"><a name="BHMcat">Catalogue Mode</a></p>

    <p>
      $BHMcalc comes along with a selection of real binary systems to
      play with.  We call this selection the <b>BHM Catalogue</b>.
      The catalogue includes those binaries where real planetary
      systems have been discovered, a set of moderately separated
      binaries (4 days &lt; P<sub>bin</sub> &lt; 60 days) selected
      from different spectroscopic and eclipsing binaries catalogues
      and last but not least, a list of what we have called <i>Binary
      Habitability Niches</i>, ie. binaries with properties well
      suited for the action of what we have called the <b>BHM
      mechanism</b>.
    </p>
    
    <p>
      In the catalogue mode a dynamic table with the basic properties
      of the binary systems will be load.  You will be able to sort,
      filter and search into the catalogue using the form controls at
      the beginning of the table.
    </p>

    <center>
      <div class="figure" style="width:80%">
	<img src="doc/figures/catalogue.png" width="100%"/>
	<p></p>
	<div class="caption">The BHM Catalogue dynamic table</div>
      </div>
    </center>

    <p>
      Beside browsing and filtering the binaries in the catalogue, you
      will be able to load each star, planet and the systems as a
      whole into the calculation modes.  This will allow you to play
      with the system and study the impact that different model
      parameters have in their radiation and plasma environment.
    </p>

    <p>
      Since all the objects in the catalogue has been already load
      into the $BHMcalc, they are the right place to start playing
      with the calculation modes.  So, we encorauge you to load your
      preferred system into the calculator before coming through the
      next section.  <a href="?Modes=Catalogue" target="_blank">Click
      here</a> to load the catalogue in a different tab and select a
      binary system to play with.
    </p>
    
    <p class="subtitle"><a name="CalculationModes">Calculation Modes</a></p>

    <p>
      When an object is load from the catalogue a calculation mode is
      activated.  If you click into the binary system link in the
      catalogue the <i>Interaction Mode</i> will be activated.  If
      instead you click into a star the <i>Star Mode</i> will be load.
    </p>

    <p>
      Each mode has its own set of tabs depending on its purpose.  The
      Star Mode is just intended for exploring the properties and
      evolution of single stars.  So, only the Star tab is open.
      However if the Binary Mode is load, 4 instead of 1 tab will be
      available: Star 1, Star 2, Planet and Binary itself.
    </p>

    <p>
      Each tab have the same structure: an input form and a result
      panel.
    </p>

    <center>
      <div class="figure" style="width:80%">
	<img src="doc/figures/tab.png" width="100%"/>
	<p></p>
	<div class="caption">The common structure of a calculation tab.</div>
      </div>
    </center>

    <p>
      The calculator use something called <i>AJAX</i> (Asyncrhonous
      JavaScript And XML).  This allows you to calculate something on
      backgorund without reloading the page or while you are doing
      something else in the calculator.  Great, eh?  That's precisely
      the purpose of the <b>Update</b> button.  This button lets you
      to commit a calculation after changing some value in the input
      form.  
    </p>

    <p>
      By default, when you load an already existing object, the result
      panel will not be full with the calculated results.  This is to
      avoid overloading the server.  As a result, you will need to
      update each tab once the object is load into the calculator.
    </p>

    <p>
      The calculator uses a scheme of dependencies on which a given
      object can only be calculated after other one has been
      calculated.  Thus, for instance, when you try to calculate the
      rotation and activity evolution of a binary system, the
      properties of their stars should be first updated.  Thus, when
      changing something in a system, we recommend to update first the
      more complex object.  This will probably impact the time you
      need to wait for a result but will ensure you the least clicks
      possible.  If you want to proceed safer you can better update
      each object at a time.
    </p>

    <p>
      And that's it! The rest is just play and have some fun and of
      course neat scientific results.
    </p>
    
    <p class="title">The Science of $BHMcalc</p>
    
    <p>
      
      Most of the science behind $BHMcalc is fully explained in the
      papers motivating its creation in the first place (see the
      <a href="?TABID=0#References">references section</a> in the Main
      tab).  We have "steal" a bunch of great astrophyical models and
      data from other researchers, to create this tool.  Anything you
      can find here will incomplete by far.  We provide here some
      details on the science behind the calculator, especially
      intended to understand some of the input information required to
      use the calculator.

    </p>

    <p class="subtitle">Stellar Models</p>

    <p>
      There are several really obvious parameters (stellar ID, mass)
      but other deserves an explanations:
    </p>

    <p>
      Input parameters:
      <ul>
	<li>
	  <b>Metallicity</b> (Z, [Fe/H]): You can provide
	  metallicity in two different forms.  By indicating the
	  fraction of metals (Z) or the amount of iron relative to the
	  Sun.  When one of them is changed the form automatically sets
	  the other one assuming a sun scaled value of the Helum
	  fraction Y.
	</li>
	<br/>

	<li>
	  <b>Stellar Model</b>: Nowadays a significant number of
	  stellar evolution models, are available in the literature.
	  Most of them have fundamental differences and more
	  importantly have subtle (and sometimes not so subtle)
	  differences in the predicted properties, we have compiled
	  results from at least 4 stellar evolution models.  The
	  models in the calculator contain evolutionary tracks for
	  stars with different metallicities and masses.  In order to
	  avoid interpolation issues the calculator selects the
	  ecolutionary track closer to the mass and metallicity
	  provided with the input form.
	</li>
	<br/>

	<li>
	  <b>PMS period</b>: Period of rotation during the pre main
	  sequence phase.
	</li>
	<br/>

	<li>
	  <b>Saturation period</b>: period of rotation at which the
	  magnetic activity of the star is saturated.  It is expressed
	  as factor of the present rotational rate of the Sun.
	</li>
	<br/>

	<li>
	  <b>Wind torque scaling</b>: The constant of proportionality
	  in the magnetic torque law.  It is determined by fitting the
	  rotational evolution of the sun to its present value..
	</li>
	<br/>

	<li>
	  <b>Disk age</b>: Age of the circumstellar disk.  It is
	  assumed that the disk provide a way to lock the angular
	  momentum evolution of the star during the pre main sequence
	  phase.
	</li>
	<br/>
	
      </ul>
    </p>

    <p>
      <center>
	<img src="web/maw.png" width=100px/>
	Men at Work!
      </center>
    </p>
  </div>
</div>
C;
?>
