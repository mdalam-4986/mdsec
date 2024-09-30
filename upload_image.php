<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $data = json_decode(file_get_contents("php://input"), true);
    $image = $data['image'];

    // Remove the "data:image/png;base64," part
    $image = str_replace('data:image/png;base64,', '', $image);
    $image = str_replace(' ', '+', $image);
    $data = base64_decode($image);

    // Save the image to a file
    $filePath = 'snapshots/' . uniqid() . '.png'; // Change this to your desired path
    file_put_contents($filePath, $data);

    // Return a response
    echo json_encode(['status' => 'success', 'filePath' => $filePath]);
} else {
    echo json_encode(['status' => 'fail', 'message' => 'Invalid request']);
}
?>
