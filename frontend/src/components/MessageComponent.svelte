<script lang="ts">
	export let message: {
		author_nickname: string;
		time_created: string;
		content: string;
	};

	const formatDate = (dateString: string): string => {
		const date = new Date(dateString);

		const hours = date.getHours().toString().padStart(2, '0');
		const minutes = date.getMinutes().toString().padStart(2, '0');
		const day = date.getDate().toString().padStart(2, '0');
		const month = (date.getMonth() + 1).toString().padStart(2, '0');
		const year = date.getFullYear();

		return `${day}.${month}.${year} ${hours}:${minutes}`;
	};
</script>

<div class="flex flex-col bg-stone-300">
	<div class="p-2px bg-stone-400 flex items-center space-x-1.5">
		<p class="text-sm font-bold">{message.author_nickname}</p>
		<p class="text-sm inline">at {formatDate(message.time_created)}</p>
	</div>
	<p>{message.content}</p>
</div>
