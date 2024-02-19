<script>
    let c1 = -0.125,
        c2 = 0.234,
        y1 = 0.492,
        y2 = -0.133;
    let key = "abcdefghijklmnop";
    let plainText = "paragon";
    let cipherValues = [];
    let originalValues = [];
    let decryptValues = [];
    let keyResults = [];

    let c1Prime, c2Prime;
    let keyError = false,
        plainTextError = false;
    let y1Prime = 0.242,
        y2Prime = -0.955;
    let cipherText = "";
    let decryptedText = "";

    function f(x) {
        return ((x + 1) % 2) - 1;
    }

    function normalize(value) {
        return value / 256.0;
    }

    function denormalize(value) {
        return Math.round(value * 256.0);
    }

    function yEquation(x, c1_, c2_, y1_, y2_) {
        return f(normalize(x + c1_ * y1_ + c2_ * y2_));
    }

    function encrypt() {
        decryptValues = [];
        originalValues = [];
        cipherValues = [];
        keyResults = [];
        cipherText = "";
        if (key.length < 16) {
            keyError = true;
            return;
        }
        if (plainText.length < 1) {
            plainTextError = true;
            return;
        }
        plainTextError = false;
        keyError = false;

        let y = [0, 0];
        y[0] = y1;
        y[1] = y2;
        for (let i = 0; i < key.length; i++) {
            let y_n = yEquation(key.charCodeAt(i), c1, c2, y[0], y[1]);
            keyResults = [...keyResults, y_n];
            y[1] = y[0];
            y[0] = y_n;
        }
        c1Prime = keyResults[14];
        c2Prime = keyResults[15];

        y[0] = y1Prime;
        y[1] = y2Prime;
        for (let i = 0; i < plainText.length; i++) {
            originalValues = [...originalValues, plainText.charCodeAt(i)];
            let y_n = Math.round(
                denormalize(normalize(plainText.charCodeAt(i) + c1Prime * y[0] + c2Prime * y[1]))
            );

            cipherValues = [...cipherValues, y_n];

            y[1] = y[0];
            y[0] = y_n;

            let encodedChar = String.fromCharCode(y_n);
            cipherText += encodedChar;
        }
        decrypt();
    }

    function decrypt() {
        decryptedText = "";
        let y = [0, 0];
        y[0] = y1Prime;
        y[1] = y2Prime;
        for (let i = 0; i < cipherText.length; i++) {
            let x_n = Math.round(
                denormalize(normalize(cipherText.charCodeAt(i) - c1Prime * y[0] - c2Prime * y[1]))
            );
            decryptValues = [...decryptValues, x_n];

            y[1] = y[0];
            y[0] = cipherText.charCodeAt(i);

            let encodedChar = String.fromCharCode(x_n);
            decryptedText += encodedChar;
        }
        console.log(decryptedText);
    }
</script>

<div class="w-full bg-zinc-800 grid"> 
    <div class="bg-zinc-600 p-3">
        <nav class="text-black p-1">
            <div class="bg-zinc-800 p-10 ">
                <h2 class="mb-10 font-bold text-2xl text-zinc-200 before:block before:absolute before:bg-zinc-900 relative text-center">Encryption Types :</h2>
                <div class="flex items-center justify-between">
                    <a class="bg-gradient-to-b w-max mx-auto text-zinc-900 font-semibold from-slate-50 to-zinc-100 px-10 py-3 rounded-2xl shadow-zinc-400 shadow-md border-b-4 hover border-b border-zinc-400 hover:shadow-sm transition-all duration-500" href="/">Text Encryption</a>
                    <a class="bg-gradient-to-b w-max mx-auto text-zinc-900 font-semibold from-slate-50 to-zinc-100 px-10 py-3 rounded-2xl shadow-zinc-400 shadow-md border-b-4 hover border-b border-zinc-400 hover:shadow-sm transition-all duration-500" href="/image">Image Encryption</a>
                    <a class="bg-gradient-to-b w-max mx-auto text-zinc-900 font-semibold from-slate-50 to-zinc-100 px-10 py-3 rounded-2xl shadow-zinc-400 shadow-md border-b-4 hover border-b border-zinc-400 hover:shadow-sm transition-all duration-500" href="/audio">Audio Encryption</a>
                    <a class="bg-gradient-to-b w-max mx-auto text-zinc-900 font-semibold from-slate-50 to-zinc-100 px-10 py-3 rounded-2xl shadow-zinc-400 shadow-md border-b-4 hover border-b border-zinc-400 hover:shadow-sm transition-all duration-500" href="/video">Video Encryption</a>
                </div>  
            </div>
        </nav>
    </div>
    <!-- number inputs -->
    <div class="p-10 flex-wrap gap-6 flex justify-between ">
    <form action="" class="bg-zinc-800 text-white rounded-lg p-5 flex flex-col gap-4">
        <h1 class="font-bold text-zinc-200">Input values for C1 and C2 </h1>
        <div class="flex gap-4 items-center">
            <h3 class="font-bold">C1:</h3>
            <input
                bind:value={c1}
                type="number"
                step="0.001"
                class="bg-zinc-700 rounded-md px-2 py-3"
            />
        </div>
        <div class="flex gap-4 items-center">
            <h3 class="font-bold">C2:</h3>
            <input
                bind:value={c2}
                type="number"
                step="0.001"
                class="bg-zinc-700 rounded-md px-2 py-3"
            />
        </div>
        
    </form>
    <!-- keys and text inputs -->
    <form action="" class="bg-zinc-800 text-white rounded-lg p-5 flex flex-col gap-4">
        <h1 class="font-bold text-zinc-200">Input values for Y(-1), Y(-2) </h1>
        <div class="flex gap-4 items-center">
            <h3 class="font-bold">Y(-1):</h3>
            <input
                bind:value={y1}
                type="number"
                step="0.001"
                class="bg-zinc-700 rounded-md px-2 py-3"
            />
        </div>

        <div class="flex gap-4 items-center">
            <h3 class="font-bold">Y(-2):</h3>
            <input
                bind:value={y2}
                type="number"
                step="0.001"
                class="bg-zinc-700 rounded-md px-2 py-3"
            />
        </div>
        
    </form> <form action="" class="bg-zinc-800 text-white rounded-lg p-5 flex flex-col gap-4">
        <h1 class="font-bold text-zinc-200">Input values for Y(-1)', Y(-2)'</h1>
        <div class="flex gap-4 items-center">
            <h3 class="font-bold">Y(-1)':
            </h3>
            <input
                bind:value={y1Prime}
                type="number"
                step="0.001"
                class="bg-zinc-700 rounded-md px-2 py-3"
            />
        </div>
        <div class="flex gap-4 items-center">
            <h3 class="font-bold">Y(-2)':
            </h3>
            <input
                bind:value={y2Prime}
                type="number"
                step="0.001"
                class="bg-zinc-700 rounded-md px-2 py-3"
            />
        </div>
    </form>

    <!-- bg-zinc-800 text-white rounded-lg p-5 flex flex-col gap-4 -->
    <form action="" class="grid grid-rows-3 grid-col-3 grid-flow-col text-zinc-200 rounded-lg p-5 flex-col gap-4">
        <div class="lex gap-4 items-center">
            <h3 class=" font-bold text-zinc-200">Please Input a keys (16 Characters):</h3>
                    <input
                        maxlength="16"
                        bind:value={key}
                        type="text"
                        class="w-full mt-2 bg-zinc-700 rounded-md px-2 py-3"
                    />
                    {#if keyError}
                        <h3 class="text-red-500">
                            keys Must be 16 characters long
                        </h3>
                    {/if}
        </div>
        <div>
            <h3 class="font-bold text-zinc-200">Input a Plain Text</h3>
                    <input
                        bind:value={plainText}
                        type="text"
                        class="w-full mt-2 bg-zinc-700 rounded-md px-2 py-3"
                    />
                    {#if plainTextError}
                        <h3 class="text-red-500">
                            Plain Text must not be empty
                        </h3>
                    {/if}
        </div>
                <button
                    on:click={encrypt}
                    class="px-2 py-1 bg-zinc-500 text-zinc-200 rounded-md font-bold">
                    Encrypt
                </button>
    </form>

    <div class="grid grid-cols-3 gap-4 w-full min-h-[50vh]  ">
        <!-- First Section -->
        <section class="w-full p-1 bg-zinc-600 rounded-lg ">
            <h1 class="font-bold text-lg text-zinc-200">Keys System</h1>
            {#each Array(keyResults.length) as _, i}
                {#if i == 14}
                    <h4 class="text-zinc-200 font-bold">
                        Index: 14; c1' = {c1Prime}
                    </h4>
                {:else if i == 15}
                    <h4 class="text-zinc-200 font-bold">
                        Index: 15; c2' = {c2Prime}
                    </h4>
                {:else}
                    <h4 class="text-zinc-200">
                        <span class="font-bold">Index: {i};</span>
                        {keyResults[i]}
                    </h4>
                {/if}
            {/each}
        </section>
    
        <!-- Second Section -->
        <section class="w-full p-1 bg-zinc-600 rounded-lg p-5">
            <h1 class="font-bold text-lg text-zinc-200">Main Algorithm</h1>
            <div>
                <h2 class="text-zinc-200 font-bold">Original Values</h2>
                {#each originalValues as value}
                    <h3 class="text-zinc-200">{value}</h3>
                {/each}
            </div>
            <div>
                <h2 class="text-zinc-200 font-bold">Cipher Values</h2>
                {#each cipherValues as value}
                    <h3 class="text-zinc-200">{value}</h3>
                {/each}
            </div>
            <div>
                <h2 class="text-zinc-200 font-bold">Decrypt Values</h2>
                {#each decryptValues as value}
                    <h3 class="text-zinc-200">{value}</h3>
                {/each}
            </div>
    
        </section>
        <section class="w-full p-1 bg-zinc-600 rounded-lg p-5">
            <h2 class="text-zinc-200">
                <span class="font-bold">Encrypted Text</span>
                : {cipherText}
            </h2>
            <h2 class="text-zinc-200">
                <span class="font-bold">Decrypted Text</span>
                : {decryptedText}
            </h2>
        </section>
    </div>
    
</div>
</div>