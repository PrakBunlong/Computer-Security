<script>
  import { writable } from 'svelte/store';

  const key = writable('');
  const result = writable('');
  const uploadedImage = writable(null);
  const encryptedImagePath = writable('');
  const decryptedImagePath = writable('');

  const encrypt = async () => {
    const keyData = { key: $key, filename: $uploadedImage.name };
    
    try {
      const formData = new FormData();
      formData.append('image', $uploadedImage);

      const response = await fetch('/api/encrypt', {
        method: 'POST',
        body: formData,
      });

      const encryptedData = await response.json();
      $encryptedImagePath = encryptedData.encrypted_image_path;
    } catch (error) {
      console.error('Encryption failed', error);
    }
  };

  const decrypt = async () => {
    const keyData = { key: $key, encrypted_image_path: $encryptedImagePath };
    
    try {
      const response = await fetch('/api/decrypt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(keyData),
      });

      const decryptedData = await response.json();
      $decryptedImagePath = decryptedData.decrypted_image_path;
    } catch (error) {
      console.error('Decryption failed', error);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    $uploadedImage = file;
  };
</script>

<main>
  <label>
    Key:
    <input bind:value={$key} />
  </label>

  <input type="file" on:change={handleFileUpload} />

  <button on:click={encrypt}>Encrypt</button>
  <button on:click={decrypt}>Decrypt</button>

  <p>Encrypted Image Path: {$encryptedImagePath}</p>
  <p>Decrypted Image Path: {$decryptedImagePath}</p>
</main>
