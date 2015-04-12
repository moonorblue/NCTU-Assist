<?php
$fileName = $_GET["filename"];
$fileNames = explode(" ",$fileName);
$fileName = $fileNames[0]."\ ".$fileNames[1].".txt";
//echo $fileName;
$cmd = shell_exec("python ExtractAndInfer.py $fileName");
if($cmd){
echo $cmd;
}
else{
echo "{error:0}";
}
?>
