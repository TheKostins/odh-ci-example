<script lang="ts">
	import InputWithButton from '../components/InputWithButton.svelte';
	import type { Topic, TopicsResponse } from '../api/types.ts';
	import { onMount } from 'svelte';

	let topics = $state([] as Topic[]);
	onMount(async () => {
		const response = await fetch('/api/v1/topics');
		const data = (await response.json()) as TopicsResponse;
		topics = data.items;
	});

	const handleSearch = (name: string) => {
		if (name) {
			fetch(`/api/v1/topics?name=${name}`)
				.then((response) => response.json())
				.then((data) => data as Topic[])
				.then((data) => {
					topics = data;
				});
		} else {
			fetch(`/api/v1/topics1`)
				.then((response) => response.json())
				.then((data) => data as TopicsResponse)
				.then((data) => {
					topics = data.items;
				});
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
