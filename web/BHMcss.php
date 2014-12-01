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
font-size:16px;
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
 font-size:16px;
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
width:55%;
height:100%;
//background:lightyellow;
}
.formarea{
float:left;
width:45%;
height:100%;
//background:lightgreen;
}
.status{
float:right;
width:45%;
height:20%;
//background:lightblue;
}
.catalogue{
float:left;
width:100%;
height:100%;
 border:1px solid black;
//background:lightyellow;
}

/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
/*FORM TABLE*/
/*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*/
td.name{
 font-weight:bold;
 font-size:12px;
 padding:10px;
}
td.section{
 background:lightgray;
 text-align:center;
 font-weight:bold;
 font-size:12px;
}
td.field{
 padding:10px;
 font-size:10px;
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
 top:40px;
 right:30px;
}
button.mode{
 font-size:20px;
 padding:20px;
 width:200px;
 margin:5px;
}
a.force{
 position:absolute;
 top:65px;
 right:30px;
 font-size:10px;
}

input.cat{
 background:white;
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
 top:40px;
 right:90px;
 display:none;
 font-size:12px
}

div.stdout{
 position:absolute;
 background:white;
 padding:2px;
 border:solid black 1px;
 z-index=100;
 top:40px;
 left:45%;
 display:none;
 font-size:12px
}

a.activelink{
  text-weight:bold;
}

div.target{
 padding:10px;
 width:90%;
 //height:3ex;
 overflow:auto;
 white-space:nowrap;
 background:lightgray;
 //background:lightyellow;
 display:none;
}

div.listconfig{
 padding:10px;
 width:90%;
 //height:3ex;
 overflow:auto;
 white-space:nowrap;
  //background:lightgray;
 //background:lightyellow;
 display:block;
}

td.field_cat{
  font-size:11px;
}
tr.header{
 background:gray;
 color:white;
 font-weight:bold;
}
tr.row_light{
 background:white;
}
tr.row_dark{
 background:lightgray;
}
div.help{
 font-style:italic;
 display:block;
 font-size:12px;
 background:lightyellow;
 padding:10px;
}
div.footer{
 font-size:10px;
 font-style:italic;
 text-align:center;
}

p.title{
  font-size:16px;
  font-weight:bold;
 background:lightgray;
 padding:5px;
}

p.subtitle{
  font-size:14px;
  font-weight:bold;
  text-decoration:underline;
}

div.figure{
 border:solid lightgray 1px;
 text-align:center;
 width:40%;
 padding:10px;
}

div.caption{
  font-style:italic;
  font-size:12px;
  text-align:center;
}

li.summaryitem{
 padding:5px;
}

div.decoration{
 float:left;
 width:30%;
 padding:10px;
}

</style>
CSS;
?>
