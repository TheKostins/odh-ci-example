import type { TopicsResponse } from '../api/types';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch }) => {
	const res = await fetch('/api/v1/topics');
	const topics: TopicsResponse = await res.json();

	return {
		topics
	};
};
