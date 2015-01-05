<?PHP
$VERSION=rtrim(shell_exec("make version"));
$CHANGESLOG=rtrim(shell_exec("cat ChangesLog"));
$about=<<<C
<div class="tabbertab" id="Introduction" title="About">
  <div class="tabcontent">
    <p>
      $BHMcalc is the result of the fruitful collaboration between the
      group of
      <b>Prof. Paul Mason</b> in
      the <a href="http://academics.utep.edu/Default.aspx?tabid=18742">University
      of Texas, El Paso</a> and the group of <b>Prof. Jorge
      I. Zuluaga</b>,
      the <a href="http://urania.udea.edu.co/facom">Computational
      Physics and Astrophysics Group</a> of the University of
      Antioquia (Medell&iacute;n, Colombia).
    </p>
  
    <a name="References"></a>
    <p>
      To cite $BHMcalc please refer to one or all of the following
      papers:

      <ul>

	<li>
	  <a href="http://arxiv.org/abs/1501.00296">[Zuluaga+2015]</a>
	  Zuluaga, J.I., Mason, P.A. & Cuartas-Restrepo,
	  P. A. (2015). <i>Constraining the Radiation and Plasma
	  Environment of Kepler Circumbinary habitable zone
	  planets</i>. <b>Submitted to the Astrophysical Journal</b> (<a href="http://arxiv.org/abs/1501.00296">arXiv:1501.00296</a>).
	</li>

	<br/>
	<li>
	  <a href="http://adsabs.harvard.edu/abs/2013ApJ...774L..26M">[Mason+2013]</a>
	  Mason, P. A., Zuluaga, J. I., Clark, J. M., &
	  Cuartas-Restrepo, P. A. (2013). <i>Rotational Synchronization
	  May Enhance Habitability for Circumbinary Planets: Kepler
	  Binary Case Studies</i>. <b>The Astrophysical Journal Letters</b>,
	  774(2), L26. (ADS:
	  2013ApJ...774L..26M, <a href="http://arxiv.org/abs/1307.4624">arXiv:1307.4624</a>)
	</li>
	<br/>
	<li>
	  <a href="http://adsabs.harvard.edu/abs/2014arXiv1408.5163M">[Mason+2014]</a>
	  Mason, P. A., Zuluaga, J. I., Cuartas-Restrepo, P. A., &
	  Clark, J. M. (2014). Circumbinary Habitability
	  Niches. <b>International Journal of Astrobiology</b>.  (ADS:
	  2014arXiv1408.5163M, <a href="http://arxiv.org/abs/1408.5163">arXiv:1408.5163</a>)
	</li>
      </ul>	  
    </p>
    
    <p>
      This is the second version of the $BHMcalc.  A previous and
      simpler version of the tool was released along
      the <b>[Mason+2014]</b> paper and it is presently unavailable.
    </p>
    
    <p class="title">Version</p>
    <pre>$VERSION</pre>

    <p class="title">Changes Log</p>
    <p>
    $CHANGESLOG
    </p>
    
  </div>
</div>
C;
?>
