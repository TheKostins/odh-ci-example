import type { PageLoad } from './$types';

interface Topic {
	id: number;
	name: string;
}

interface Message {
	author_nickname: string;
	content: string;
	time_created: string;
}

interface MessagesResponse {
	limit: number;
	offset: number;
	total: number;
	items: Message[];
}

export const load: PageLoad = async ({ fetch, params }) => {
	const topic_res = await fetch(`/api/v1/topics/${params.id}`);
	const topic: Topic = await topic_res.json();

	const messages_res = await fetch(`/api/v1/topics/${params.id}/messages`);
	const messages: MessagesResponse = await messages_res.json();

	return {
		topic,
		messages
	};
};
