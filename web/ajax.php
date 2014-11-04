<?
sleep(1);
print_r($_GET);
$nombre=$_GET["nombre"];
echo "Listo $nombre";
shell_exec("echo 'Nombre: $nombre' > /tmp/a");
?>