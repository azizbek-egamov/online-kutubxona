<?php

function captcha($num){
$image_x = 200;
$image_y = 50;
$font_size = 30;
$img = imagecreatetruecolor($image_x, $image_y);
$bg_color = imagecolorallocate($img, 255, 255, 255);
imagefill($img, 0, 0, $bg_color);
$text_color = imagecolorallocate($img, 0, 0, 0);
for($i=0; $i<15; $i++){
$line_color = imagecolorallocate($img,rand(0, 255),rand(0, 255),rand(0, 255));
imageline($img,rand(0,$image_x),rand(0,$image_y),rand(0,$image_x),rand(0, $image_y),$line_color);
}
$text_x = 50;
$text_y = ($image_y/2)+($font_size/2);
imagettftext($img,$font_size,0,$text_x,$text_y,$text_color,'font/font.ttf',$num);
header('Content-type: image/png');
imagepng($img);
imagedestroy($img);
}

if (isset($_GET['text'])) {
    captcha($_GET['text']);
} else {
    echo "false";
}

?>