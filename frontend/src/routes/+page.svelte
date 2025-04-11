<script lang="ts">
	import InputWithButton from '../components/InputWithButton.svelte';
	import type { PageProps } from './$types';
	import type { Topic } from '../api/types.ts';
	let { data }: PageProps = $props();

	let topics = $state(data.topics.items);

	const handleSearch = (name: string) => {
		if (name) {
			fetch(`/api/v1/topics?name=${name}`)
				.then((response) => response.json())
				.then((data) => data as Topic[])
				.then((data) => {
					topics = data;
				});
		} else {
			topics = data.topics.items;
		}
	};

	const handleCreateTopic = (name: string) => {
		if (name) {
			fetch('/api/v1/topics', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ name: name })
			})
				.then((response) => response.json())
				.then((data) => data as Topic)
				.then((data) => {
					topics = [data, ...topics];
				});
		}
	};
</script>

<div class="w-full h-20 flex justify-center items-center">
	<h1 class="text-2xl font-bold text-center text-gray-800">Добро пожаловать на 3.5 чан!</h1>
</div>

<div class="h-max flex flex-col pl-20 space-y-2">
	<div class="flex space-x-5 items-center">
		<p class="text-xl">Список топиков</p>
		<div class="flex flex-col space-y-2">
			<InputWithButton placehoder="Найти по названию" buttonText="Поиск" onClick={handleSearch} />
			<InputWithButton
				placehoder="Создать топик"
				buttonText="Создать"
				onClick={handleCreateTopic}
			/>
		</div>
	</div>
	<div class="flex flex-col space-y-2">
		{#each topics as topic (topic.id)}
			<div class="flex items-center space-x-2">
				<a class="text-lg" href="/topics/{topic.id}">{topic.name}</a>
			</div>
		{/each}
	</div>
</div>
