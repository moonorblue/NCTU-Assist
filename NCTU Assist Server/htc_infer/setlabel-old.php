<?php
$fileName = $_GET["filename"];
$fileNames = explode(" ",$fileName);
$fileName = $fileNames[0]."\ ".$fileNames[1].".txt";
$userId = explode("_",$fileNames[1]);
$label = $_GET["label"];
//echo "python SetLabel.py $fileName $label<br>";
echo "python SetLabel.py $fileName $userId[1] $label<br>";
$cmd = shell_exec("python Setlabel.py $fileName $userId[1] $label");
if($cmd){
echo $cmd;
}
else{
echo "error";
}
?>
