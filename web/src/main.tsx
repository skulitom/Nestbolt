import { render } from 'preact';
import { App } from './app';
import './styles.css';

const root = document.getElementById('app')!;
// index.html shows a static skeleton until the app is ready.
root.textContent = '';
render(<App />, root);
