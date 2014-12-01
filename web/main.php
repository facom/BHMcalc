<?PHP
$main=<<<C
<div class="tabbertab" id="Introduction" title="Main">
  <div class="tabcontent">
    
    <p>
      Welcome to the <b>Binary Habitability Calculator</b>, $BHMcalc!
    </p>

    <p>
      Please select which <a href="?HELP#Modes">$BHMcalc Mode</a> you
      want to use:
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

    <p>
      The $BHMcalc is a web application intended to explore the vast
      configuration space of <b><i>Circumbinary Planetary System</i>
      </b> (aka. <i>Tatooines</i>), their physical properties,
      evolution and the details of the complex interaction between a
      pair of close stars and the planets around.
    </p>

    <p>
      This tool is intended to <b>gain insights</b> about the complex
      landscape of circumbinary planets and their potentially
      habitable environments.  <b>$BHMcalc is not aimed to provide
      detailed predictions</b> about actual circumbinary systems.
      However, if it is used properly their results could provide
      useful constraints for already existing planetary systems.
    </p>

    <p>
      $BHMcalc is the result of the collaboration between the group of
      <b>Prof. Paul Mason</b> in the New Mexico State University and
      the <a href="http://urania.udea.edu.co/facom">Computational
      Physics and Astrophysics Group</a> of the University of
      Antioquia (Medell&iacute;n, Colombia) lead by <b>Prof. Jorge
      I. Zuluaga</b>.
    </p>

    <a name="References"></a>
    <p>
      If you are using the $BHMcalc for <b>research purposes</b> do
      not forget to <b style='color:red'>cite properly the scientific
      literature on which it is based</b>.  When citing $BHMcalc
      please refer to the following published literature:
      <ul>
	<li>
	  <a href="http://adsabs.harvard.edu/abs/2013ApJ...774L..26M">[Mason+2013]</a>
	  Mason, P. A., Zuluaga, J. I., Clark, J. M., &
	  Cuartas-Restrepo, P. A. (2013). <i>Rotational Synchronization
	  May Enhance Habitability for Circumbinary Planets: Kepler
	  Binary Case Studies</i>. <b>The Astrophysical Journal Letters</b>,
	  774(2), L26. (ADS:
	  2013ApJ...774L..26M, <a href="http://arxiv.org/abs/1307.4624">arXiv:1307.4624</a>)
	</li>
	<li>
	  <a href="http://adsabs.harvard.edu/abs/2014arXiv1408.5163M">[Mason+2014]</a>
	  Mason, P. A., Zuluaga, J. I., Cuartas-Restrepo, P. A., &
	  Clark, J. M. (2014). Circumbinary Habitability
	  Niches. Accepted for publication in the International
	  Journal of Astrobiology.  (ADS:
	  2014arXiv1408.5163M, <a href="http://arxiv.org/abs/1408.5163">arXiv:1408.5163</a>)
	</li>
      </ul>	  
    </p>

    <p class="title">Gallery</p>
    <p>

    <div class="decoration">
      <a href="$wDIR/web/gallery/sunset.jpg">
	<img src="$wDIR/web/gallery/sunset.jpg" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Sunset. Credit: Paramount Pictures/CBS Studios. <a href="http://en.memory-alpha.org/wiki/File:Risan_sunset.jpg">Source</a>
      </div>
    </div>

    <div class="decoration">
      <a href="$wDIR/web/gallery/wondering.png">
	<img src="$wDIR/web/gallery/wondering.png" width="100%"/>
      </a>
      <br/>
      <div class="caption">
	Is there life around single stars?. Credit: Alejandro Rua, Medellin, Colombia.
      </div>
    </div>

    </p>
  </div>
</div>
C;
?>
