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
      the <a href="http://academics.utep.edu/Default.aspx?tabid=18742"
      target="_blank">University of Texas, El Paso</a> and <b>New
      Mexico State University</b> and the group of <b>Prof. Jorge
      I. Zuluaga</b>, the <a href="http://urania.udea.edu.co/facom"
      target="_blank">Computational Physics and Astrophysics Group</a>
      of the <a href="http://www.udea.edu.co">University of
      Antioquia</a> (Medell&iacute;n, Colombia).  Other colleagues
      directly involved are <b>Dr. Pablo Cuartas</b> (FACom/UdeA)
      and <b>Joni Clark</b> (NMSU).
    </p>
  
    <a name="References"></a>
    <p>
      To cite $BHMcalc please refer to one or all of the following
      papers:

      <ul>

	<li>
	  <a href="http://arxiv.org/abs/1501.00296" target="_blank">[Zuluaga+2015]</a>
	  Zuluaga, J.I., Mason, P.A. & Cuartas-Restrepo,
	  P. A. (2015). <i>Constraining the Radiation and Plasma
	  Environment of Kepler Circumbinary habitable zone
	  planets</i>. <b>Submitted to the Astrophysical Journal</b> (<a href="http://arxiv.org/abs/1501.00296" target="_blank">arXiv:1501.00296</a>).
	</li>

	<br/>

	<li>
	  <a href="http://adsabs.harvard.edu/abs/2014arXiv1408.5163M" target="_blank">[Mason+2014]</a>
	  Mason, P. A., Zuluaga, J. I., Cuartas-Restrepo, P. A., &
	  Clark, J. M. (2014). Circumbinary Habitability
	  Niches. <b>International Journal of Astrobiology</b>.  (ADS:
	  2014arXiv1408.5163M, <a href="http://arxiv.org/abs/1408.5163" target="_blank">arXiv:1408.5163</a>)
	</li>
	<br/>

	<li>
	  <a href="http://adsabs.harvard.edu/abs/2013ApJ...774L..26M" target="_blank">[Mason+2013]</a>
	  Mason, P. A., Zuluaga, J. I., Clark, J. M., &
	  Cuartas-Restrepo, P. A. (2013). <i>Rotational Synchronization
	  May Enhance Habitability for Circumbinary Planets: Kepler
	  Binary Case Studies</i>. <b>The Astrophysical Journal Letters</b>,
	  774(2), L26. (ADS:
	  2013ApJ...774L..26M, <a href="http://arxiv.org/abs/1307.4624" target="_blank">arXiv:1307.4624</a>)
	</li>

      </ul>	  
    </p>
    
    <p>
      This is the second version of the $BHMcalc.  A previous and
      simpler version of the tool was released along
      the <b>[Mason+2014]</b> paper and it is presently unavailable.
    </p>

    <a name="Acknowledgement"></a>
    <p class="title">Acknowledgements</p>

    <p>
      $BHMcalc is made possible thanks to the support and the direct
      as well as indirect participation of several institutions and
      colleagues.<br/><br/>

      Firstly we thank to <b>W. Welsh</b>, <b>N. Haghighapor</b>, <b>G. Torres</b>,
      <b>S. Cranmer</b> and <b>A. Claret</b> for useful discussions
      and insightful comments regarding the models applied in the
      calculator.  <b>I. Baraffe</b> provided several key results for
      modeling the evolution of stellar rotation of low
      mass-stars.<br/><br/>

      Jorge I. Zuluaga thanks the <b>Harvard-Smithsonian Center for
      Astrophysics</b> for their hospitality during a 5 months stay in
      the fall/winter 2014-2015 where most of the major improvements
      of the calculator were achieved.  Thanks to <b>Prof. Dimitar
      Sasselov</b> for the invitation.<br/><br/>

      The Calculator has been developed under the financial support
      of: <b>Fulbright Commission, Colombia</b>, the <b>Vicerrectoria
      de Docencia / Facultad de Ciencias Exactas y Naturales /
      Instituto de Fisica</b> of the University of Antioquia and the
      program of <b>Sostenibilidad/CODI/UdeA</b>.<br/><br/>

      Special thanks to <b>Steffen Christensen</b> for testing the
      tool and finding several major bugs.<br/><br/>
      
    </p>
    
    <a name="Version"></a>
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
