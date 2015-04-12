<?php
$fileName = $_GET["filename"];
$fileNames = explode(" ",$fileName);
$userId = explode("_",$fileNames[1]);
$cmd = shell_exec("python remove.py $fileName");
if($cmd){
echo $cmd;
}
else{
echo "error";
}
?>
