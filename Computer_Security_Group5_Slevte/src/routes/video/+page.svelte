<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Encryption</title>
    <!-- Include Tailwind CSS from CDN -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/ffmpeg/0.12.10/umd/ffmpeg.min.js" integrity="sha512-j2FJMGBh+AdPWKCKDqIzH67vu4ps8OsNZqqetz8YSlbwy2ZwFTL+p6Hp1j17nL0B7IDl9E4zhPUXZKwz7MzjQQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="/assets/util/package/dist/umd/index.js"></script>

</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4">
        <h3 class="text-lg font-semibold text-gray-700 mb-4">Upload a video to encrypt and play!</h3>
        <!-- svelte-ignore a11y-media-has-caption -->
        <video id="output-video" controls class="mx-auto mb-4"></video><br/>
        <input type="file" id="uploader" class="mb-4">
        <button id="encrypt-button" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-4">
            Encrypt Video
        </button>
        <p id="message" class="text-sm text-gray-500 mb-4"></p>
        <script>
          const { fetchFile } = FFmpegUtil;
          const { createFFmpeg } = FFmpeg;
          let ffmpeg = null;
          const loadFFmpeg = async () => {
        if (ffmpeg === null) {
          ffmpeg = createFFmpeg({ log: true });
          await ffmpeg.load({
            coreURL: "/assets/core/package/dist/umd/ffmpeg-core.js",
          });
        }
      };

      const encryptVideo =
async (files) => {
const message = document.getElementById('message');
const encryptButton = document.getElementById('encrypt-button');
encryptButton.textContent = 'Encrypting...';
        encryptButton.disabled = true;
        message.textContent = 'Loading FFmpeg core...';

        if (ffmpeg === null) {
          ffmpeg = createFFmpeg({
            log: true,
          });
          ffmpeg.on('progress', ({ ratio }) => {
            message.textContent = `Progress: ${(ratio * 100.0).toFixed(2)}%`;
          });
        }

        try {
             // Check if FFmpeg has been loaded
             if (!ffmpeg.isLoaded()) {
                await ffmpeg.load();
              }

              const { name } = files[0];
              message.textContent = 'Uploading video...';

              // Write the video file to FFmpeg's virtual file system
              await ffmpeg.write(name, await fetchFile(files[0]));

              message.textContent = 'Extracting frames...';
              // This command extracts frames at a rate of 1 per second (you can adjust this rate)
              await ffmpeg.run('-i', name, '-vf', 'fps=1', 'frame_%04d.png');

              // Here you would insert the logic for your encryption algorithm
              // For the purposes of this example, we're just renaming the frames
              const frameFiles = ffmpeg.FS('readdir', '/').filter(file => file.startsWith('frame_'));
              for (let i = 0; i < frameFiles.length; i++) {
                // Read the file data
                const frameData = ffmpeg.FS('readFile', frameFiles[i]);
                // Apply your encryption logic to frameData here
                // For now, we will simply invert the colors as a placeholder for encryption
                for (let j = 0; j < frameData.length; j += 4) {
                  frameData[j] = 255 - frameData[j];     // Red
                  frameData[j + 1] = 255 - frameData[j + 1]; // Green
                  frameData[j + 2] = 255 - frameData[j + 2]; // Blue
                  // Alpha channel is frameData[j + 3], we don't need to change this
                }
                // Write the 'encrypted' frame back
                ffmpeg.FS('writeFile', `
encrypted_frame_${String(i).padStart(4, '0')}.png`, frameData);
}
message.textContent = 'Reassembling video...';
          // This command reassembles the 'encrypted' frames into a video
          await ffmpeg.run('-f', 'image2', '-framerate', '1', '-i', 'encrypted_frame_%04d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'encrypted_video.mp4');

          // Read the result and create the URL for downloading
          const encryptedVideoData = ffmpeg.FS('readFile', 'encrypted_video.mp4');
          const video = document.getElementById('output-video');
          video.src = URL.createObjectURL(new Blob([encryptedVideoData.buffer], { type: 'video/mp4' }));

          message.textContent = 'Encryption complete!';
          encryptButton.textContent = 'Encrypt Video';
          encryptButton.disabled = false;
        } catch (e) {
          console.error('Error encrypting the video:', e);
          message.textContent = 'An error occurred during the encryption process.';
          encryptButton.textContent = 'Encrypt Video';
          encryptButton.disabled = false;
        }
      };

      // Event listener for the file uploader
      const uploader = document.getElementById('uploader');
      uploader.addEventListener('change', (event) => {
        const files = event.target.files;
        if (files.length > 0) {
          loadFFmpeg().then(() => {
            encryptVideo(files);
          });
        }
      });

      // Event listener for the encrypt button
      const encryptButton = document.getElementById('encrypt-button');
      encryptButton.addEventListener('click', () => {
        if
(uploader.files.length > 0) {
encryptVideo(uploader.files);
} else {
message.textContent = 'Please select a video file first.';
}
});
</script>
</div>

</body>
</html>
