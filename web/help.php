<?PHP
$help=<<<C
<div class="tabbertab" id="Introduction" title="Help">
  <div class="tabcontent">
    
    <p class="title">Help topics</p>

    <p>
      <ul>
	<li><a href="?HELP#Presentation">Presentation</a></li>
	<li>
	  <a href="?HELP#QuickStart">Quick Start</a>
	  <ul>
	    <li><a href="?HELP#BHMCatalogue">The BHM Catalogue</a></li>
	    <li><a href="?HELP#CalculationModes">Calculation Modes</a></li>
	  </ul>
	</li>
	<li><a href="?HELP#Gallery">Snapshots and Gallery</a></li>
      </ul>
    </p>

    <p class="title"><a name="Presentation">Presentation</a></p>
    
    <img src="$wDIR/doc/figures/binaries.png" width="300px" align="left" style="margin-right:30px;margin-bottom:30px"/>

    <p>
      Thousands of planets around other stars have been discovered so
      far (for an updated list see the <a href="http://exoplanet.eu"
      target="_blank">Exoplanets Encyclopedia</a>).
      Although <b>nearly half of the stars in the Galaxy have one or
      more stellar companions</b> (binary and multiple systems), most
      of these planets have been discovered around single stars.
    </p>

    <p>
      In the last few years, the advent of very sensitive photometric
      and astrometric survey instruments (Kepler, Gaia), has finally
      allowed the discovery of the first planetary systems around
      multiple stellar systems.  Today a dozen of them have been
      catalogued and well described (see
      the <a href="?Modes=Catalogue" target="_blank">BHM Catalogue</a>
      in this website).
    </p>
    
    <p>
      Against all odds, planets can be formed and stay for billions of
      years around multiple stars.  They can either orbit only one of
      the stars in the system in a so-called <b>"s-type" orbit</b>
      (see figure), or they can orbit two close stars in a <b>"p-type"
      orbit</b> (circumbinary planets).
    </p>

    <p>
      Circumbinary Planets (planets orbiting two stars)
      or <b><i>Tatooines</i></b> as they are informally called, have
      proven to be the most interesting objects.  Not only the dynamic
      of their orbits is much more complex but the conditions they
      could face while orbiting two stars lead to astrobiological
      relevant effects.
    </p>

    <p>
      $BHMcalc is a web tool intended to explore the complex parameter
      space of Circumbinary Planets in order to <b>gain some
      insight</b> about their properties and more specifically about
      their potential to host habitable environments.  Beyond only
      helping to explore the properties of hypothetical systems, the
      calculator can also be used to <b>constraint the conditions</b>
      around already discovered circumbinary systems.
    </p>
    
    <p>
      $BHMcalc can be used to calculate/constraint:
      <ul>
	<li>
	  The evolution of basic stellar properties, radius,
	  luminosity, etc., using stellar evolutionary tracks provided
	  by different groups (Star Mode).
	</li>
	<li>
	  Rotational evolution of single stars using different
	  rotational evolutionary models (Star Mode).
	</li>
	<li>
	  Stellar activity as a function of time using the
	  Cranmer & Saar solar-inspired model (Star Mode).
	</li>
	<li>
	  Basic properties of solid and ice/gas planets (Planet
	  Mode).
	</li>
	<li>
	  Thermal evolution and magnetic properties of planets
	  with masses from super-Earths to Jovian planets (Planet
	  Mode).
	</li>
	<li>
	  Basic orbital properties of binary systems (Binary Mode).
	</li>
	<li>
	  Limits of the Circumbinary Habitable Zone (BHZ) and
	  their evolution in time (Habitable Zone Mode).
	</li>
	<li>
	  limits of the Continuous Circumbinary Habitable Zone
	  (CBHZ) and the habitability timespan of planets in
	  binaries (Habitable Zone Mode).
	</li>
	<li>
	  Insolation and Photosynthetic Photon Flux Density (PPFD) in
	  circumbinary planets (Habitable Zone Mode).
	</li>
	<li>
	  Rotational evolution of stars in binaries including
	  the effect of tidal interaction (Interaction Mode).
	</li>
	<li>
	  Evolution of activity of stars in binary systems (Interaction Mode).
	</li>
	<li>
	  Stellar wind properties (flux and dynamic pressure)
	  around moderately separated binaries (Interaction Mode).
	</li>
	<li>
	  X-ray luminosity of stars in binaries and its flux on
	  circumbinary planets (Interaction Mode).
	</li>
      </ul>
    </p>

    <p>
      $BHMcalc is specifically designed to calculate these and other
      properties in the particular case of binaries with moderate
      separations and orbital periods, i.e. 5 days &lt;
      P<sub>bin</sub> &lt; 60 days.  Although some of the tools
      available here (stellar and planetary evolution models) apply
      irrespectively binary separations, the most important modules
      are only designed for these particular systems.
    </p>

    <p class="title"><a name="QuickStart">Quick Start</a></p>

    <p>
     $BHMcalc works as a regular windows application. Its usage is
     intuitive and easy to master.
    </p>
    
    <p>
      The calculator can be used in different ways (<i>modes</i>): you
      can browse the <a href="?HELP#BHMcat">BHM catalogue</a>
      (Catalogue Mode), calculate the properties of a single star
      (Star Mode) or a planet (Planet Mode) or simply proceed to do
      the full thing (Interaction Mode), ie. calculate the property of
      stars in a binary system and their interaction with a planet.
    </p>
    <center>
      <div class="figure">
	<img src="$wDIR/doc/figures/modes.png" width="100%"/>
	<div class="caption">The Calculator Modes</div>
      </div>
    </center>
    
    <p>
      So, why don't you try the calculator while reading this
      guide.  <a href="?"  target="_blank">Click here</a> to open it
      in a new browser tab.
    </p>

    <a name="Modes"></a>
    <p class="subtitle"><a name="BHMCatalogue">Catalogue Mode</a></p>

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
      mechanism</b> [Mason+2014].
    </p>
    
    <p>
      In the Catalogue Mode a dynamic table with the basic properties
      of the binary systems will be displayed.  You will be able to
      sort, filter and search into the catalogue using the form
      controls at the top of the table.
    </p>

    <center>
      <div class="figure" style="width:80%">
	<img src="$wDIR/doc/figures/catalogue.png" width="100%"/>
	<p></p>
	<div class="caption">The BHM Catalogue dynamic table</div>
      </div>
    </center>

    <p>
      Beside browsing and filtering the binaries in the catalogue, you
      will also be able to load each star, planet or the whole system
      into the calculation modes.
    </p>

    <p>
      All the objects in the catalogue has been already load into the
      $BHMcalc.  As a result, all their properties have been already
      calculated and available to explore in depth.  This is the right
      place to start playing with the calculation modes.
    </p>

    <p>
      We encorauge you to load your preferred system into the
      calculator before going through the next
      sections.  <a href="?Modes=Catalogue" target="_blank">Click
      here</a> to load the catalogue and select a binary system to
      play with.
    </p>
    
    <p class="subtitle"><a name="CalculationModes">Calculation Modes</a></p>

    <p>
      When an object is load from the catalogue, a calculation mode is
      activated.  If you click in the binary system link
      the <i>Interaction Mode</i> will be activated.  If instead, you
      click the link of the star, the <i>Star Mode</i> will be load.
    </p>

    <p>
      Each mode has its own set of tabs depending on its purpose.  The
      Star Mode, for example, is just intended for exploring the
      properties and evolution of single stars.  So, only the Star tab
      will be open in this mode.  On the other hand, if the Binary
      Mode is load, four instead of one tabs will be available: Star
      1, Star 2, Planet and Binary itself.
    </p>

    <p>
      Each tab have the same structure: two panels, one cointanining
      an input form and the other one the result panel.
    </p>

    <center>
      <div class="figure" style="width:80%">
	<img src="$wDIR/doc/figures/tab.png" width="100%"/>
	<p></p>
	<div class="caption">The common structure of a calculation tab.</div>
      </div>
    </center>

    <p>
      The calculator use a technology called <i>AJAX</i> (Asyncrhonous
      JavaScript And XML).  This allows you to calculate something on
      backgorund without reloading the page or while you are doing
      something else in the calculator.  This is precisely the purpose
      of the <b>Update</b> button.  This button will let you to commit
      a calculation after changing some value in the input form.  You
      do not need to reload the page or expect for the calculation to
      end, to continue exploring or changing other fields in the
      calculator.
    </p>

    <p>
      By default, when you load an already existing object (an object
      from the catalogue or a configuration you have saved in your
      session directory), a new tab, the Summary tab, will be
      available.  In the summary tab, a panel with the results already
      calculated and stored in the server, will be loaded.
    </p>

    <center>
      <div class="figure" style="width:80%">
	<img src="$wDIR/doc/figures/summary.png" width="100%"/>
	<p></p>
	<div class="caption">The summary tab.</div>
      </div>
    </center>

    <p> Using the summary tab you will be able to: Download files
      related to the system (configuration, data, images). Generate a
      link to the system; you will be able to "bookmark" this link or
      send it to a collaborator. Generate the command line required to
      calculate the properties of the system using the offline
      calculator.  Save and load stored configurations; saved
      configurations will be available only in the same session of the
      browser.  If you use another browser or clean the cookies the
      session information will change.
    </p>
    
    <p>
      The calculator uses a scheme of dependencies on which a given
      object can only be calculated after other one has been
      calculated.  Thus, for instance, when you try to calculate the
      rotation and activity evolution of a binary system, the
      properties of their stars should be first updated.  Thus, when
      changing something in a system, we recommend to update first the
      more complex object first.  This will probably impact the time
      you need to wait for a result but will ensure you the least
      clicks possible.  If you want to proceed safer you can better
      update each object at a time.
    </p>

    <p>
      <center>
	<img src="web/maw.png" width=100px/><br/>
	This site is under construction.
      </center>
    </p>

    <p class="title"><a name="Gallery">Snapshots and Gallery</a></p>

    <p>
    <div class="decoration">
      <a href="$wDIR/web/gallery/stellar-rotation.png">
	<img src="$wDIR/web/gallery/stellar-rotation.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Stellar rotation evolution for the primary of Kepler-34.
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/rot-evolution.png">
	<img src="$wDIR/web/gallery/rot-evolution.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Evolution of rotation for the components of Kepler-34.
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/mass-loss-gas.png">
	<img src="$wDIR/web/gallery/mass-loss-gas.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Mass-loss from gas giants in the Habitable Zone of Niche-02
	planet.
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/flux-XUV-absolute.png">
	<img src="$wDIR/web/gallery/flux-XUV-absolute.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Flux of XUV radiation in the HZ of Niche-02.
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/standoff-distance.png">
	<img src="$wDIR/web/gallery/standoff-distance.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Magnetospheric standoff distance calculated for Kepler-35b.
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/stellar-props.png">
	<img src="$wDIR/web/gallery/stellar-props.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Evolution of KIC-9632895 using the closest PARSEC evolutionary
	track.
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/standoff-distance-earthlike.png">
	<img src="$wDIR/web/gallery/standoff-distance-earthlike.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Magnetospheric standoff radius as a function of time for an
	Earth-like planet in the middle of the BHZ of Niche-08
      </div>
    </div>
    
    <div class="decoration">
      <a href="$wDIR/web/gallery/iHZ.png">
	<img src="$wDIR/web/gallery/iHZ.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Habitable Zone of Kepler-16.
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/hz-evolution.png">
	<img src="$wDIR/web/gallery/hz-evolution.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Continuous Habitable Zone of KIC-9632895.
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/planet-schematic-gas.png">
	<img src="$wDIR/web/gallery/planet-schematic-gas.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Schematic diagram of the size and interior structure of the
	ice/gas giant Kepler-47c.
      </div>
    </div>
    
    <div class="decoration">
      <a href="$wDIR/web/gallery/planet-schematic.png">
	<img src="$wDIR/web/gallery/planet-schematic.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Schematic representation of the Earth interior as calculated
	with the Planet module.
      </div>
    </div>
    </p>
    <br/>
    <p>
    <div class="decoration">
      <a href="$wDIR/web/gallery/sunset.jpg">
	<img src="$wDIR/web/gallery/sunset.jpg" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Sunset in a Circumbinary Planet. Credit: Paramount
	Pictures/CBS
	Studios. <a href="http://en.memory-alpha.org/wiki/File:Risan_sunset.jpg">Source</a>
      </div>
    </div>
    
    <div class="decoration">
      <a href="$wDIR/web/gallery/wondering.png">
	<img src="$wDIR/web/gallery/wondering.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	"<i>Is there any life around single stars?</i>". Credit:
	Alejandro Rua, Medellin, Colombia.
      </div>
    </p>
  </div>
</div>
C;
?>
