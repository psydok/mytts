import {createWebHistory, createRouter} from "vue-router";
import vTextToSpeech from '../components/TextToSpeech.vue'
import vRating from '../components/Rating.vue'
import vAbout from '../components/About.vue'

let routes = [
    {
        path: '/',
        name: 'tts',
        component: vTextToSpeech,
        meta: { title: 'Исследование синтеза речи' }
    },
    {
        path: '/rating',
        name: 'rating',
        component: vRating,
        meta: { title: 'Рейтинг моделей' }
    },
    {
        path: '/about',
        name: 'about',
        component: vAbout,
        meta: { title: 'О технологии' }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
