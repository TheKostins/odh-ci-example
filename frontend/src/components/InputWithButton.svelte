<script lang="ts">
	export let placehoder = 'Enter text';
	export let buttonText = 'Click me!';
	let inputContents = '';
	export let onClick = (inputContets: string) => {
		console.log(`input value: ${inputContets}`);
	};
</script>

<div class="flex space-x-2">
	<input
		type="text"
		placeholder={placehoder}
		bind:value={inputContents}
		class="bg-stone-300 w-50 h-7 text-center text-stone-600"
	/>
	<button
		class="h-7 bg-stone-300 text-stone-600 pl-1 pr-1 hover:cursor-pointer w-20"
		onclick={() => onClick(inputContents)}
	>
		{buttonText}
	</button>
</div>
