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
?>
<?PHP
$linkcolor="blue";

$COLORS=array("back"=>"WHITE",
              "clear"=>"#D3D3D3",
              "front"=>"#C0C0C0",
              "text"=>"#A9A9A9",
              "shade"=>"#808080",
              "dark"=>"BLACK");

$CSS=<<<CSS
<style>
p{
font-size:12px;
}
body{
background-color:white;
font-family:Arial,Helvetica;
font-size:12px;
padding:10px;
}

a:link{
color:$linkcolor;
text-decoration:none;
}
a:visited{
color:$linkcolor;
}
a:hover{
text-decoration:underline;
}

div.title{
background-color:lightgray;
padding:10px;
border-style:outset;
border-width:2px;
}

div.form{
background-color:#B0B0B0;
padding:10px;
border-style:inset;
border-width:2px;
}

div.result{
border-style:outset;
padding:10px;
}

div.warning{
position:fixed;
right:0px;
top:0px;
border:0px solid;
border-radius:20px;
background-color:yellow;
box-shadow:10px 10px 5x black;
padding:5px;
}
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
/*TABBER*/
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
.tabberlive .tabbertabhide {
 display:none;
 }
.tabber {
 }
.tabberlive {
  margin-top:0px;
 }
ul.tabbernav
{
 margin:0px;
 padding: 3px 0;
 border-bottom: 1px solid $COLORS[dark];
 font: bold 20px Arial, Helvetica;
}
ul.tabbernav li
{
 font-size:14px;
 list-style: none;
 margin: 0;
 display: inline;
}
ul.tabbernav li a
{
 padding: 3px 0.5em;
 margin-left: 3px;
 border: 1px solid $COLORS[dark];
 border-bottom: none;
 background: $COLORS[text];
 text-decoration: none;
}
ul.tabbernav li a:link {color:$COLORS[dark];}
ul.tabbernav li a:visited {color:$COLORS[dark];}
ul.tabbernav li a:hover
{
 color:$COLORS[dark];
 background:$COLORS[text];
  border-color:$COLORS[dark];
}
ul.tabbernav li.tabberactive a
{
  background-color:#fff;
  border-bottom:3px solid #fff;
}
ul.tabbernav li.tabberactive a:hover
{
 color:$COLORS[dark];
 background:white;
 border-bottom:1px solid white;
}
.tabberlive .tabbertab {
 padding:20px;
 border:1px solid $COLORS[dark];
 border-top:0px;
 height:100%;
 overflow:auto;
 background-color:#fff;
 }
.tabberlive .tabbertab h2 {
 display:none;
 }
.tabberlive .tabbertab h3 {
 display:none;
 }
.tabberlive#tab1 {
 }
.tabberlive#tab2 {
 }
.tabberlive#tab2 .tabbertab {
 height:200px;
 overflow:auto;
 }
.maintabber{
 position:relative;
 top:0px;
 width:100%;
 margin-left:0%;
 }
.sectabber{
 position:relative;
 top:10px;
 width:96%;
 margin-left:2%;
 height:77%;
 }
.maintab {
 font-size:12px;
 height:100%;
 overflow:auto;
 }
.sectab {
 font-size:12px;
 height:100%;
 overflow:auto;
 }

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
/*FORM AREA*/
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
div {
 display: block;
}
.wrapper {
width:100%;
height:100%;
}
.results{
float:left;
width:50%;
height:100%;
//background:lightyellow;
}
.formarea{
float:left;
width:50%;
height:100%;
//background:lightgreen;
}
.status{
float:right;
width:50%;
height:20%;
//background:lightblue;
}

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
/*FORM TABLE*/
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
td.name{
 font-weight:bold;
 font-size:12px;
 padding:10px;
}
td.field{
 padding:10px;
}
td.help{
 font-style:italic;
 font-size:12px;
 padding:10px;
}
td.button{
 padding:10px;
 text-align:right;
}

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
/*INPUT*/
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
button{
  font-size:12px;
}
button.update{
 position:absolute;
 top:35px;
 right:30px;
}

input{
 background:white;
 height:30px;
 padding:2px;
}

.title{
  font-weight:bold;
  font-size:14px;
 }

iframe{
 width:100%;
 scrolling:false;
 border:0px;
}

div.download{
 position:absolute;
 background:white;
 padding:2px;
 border:solid black 1px;
 z-index=100;
 top:15%;
 right:5%;
 display:none;
}

</style>
CSS;
?>
