// Classify the exact checked-out tag before the workflow publishes any assets.
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { VERSION, root } from './build.mjs';

export function releasePolicy(tag, tags) {
  const valid = value => typeof value === 'string' && value.startsWith('v') && VERSION.test(value.slice(1));
  if (!valid(tag) || !tags.includes(tag)) throw new Error('Release requires an existing valid version tag.');
  const prerelease = tag.includes('-');
  const stable = tags.filter(value => valid(value) && !value.includes('-'));
  const compare = (a, b) => {
    const left = a.slice(1).split('.').map(BigInt), right = b.slice(1).split('.').map(BigInt);
    for (let i = 0; i < 3; i++) {
      if (left[i] !== right[i]) return left[i] < right[i] ? -1 : 1;
    }
    return 0;
  };
  stable.sort(compare);
  return { prerelease, latest: !prerelease && tag === stable.at(-1) };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    if (process.argv.length !== 3) throw new Error('Usage: node mcpb/release.mjs vX.Y.Z[-prerelease]');
    const tags = execFileSync('git', ['tag', '--list', 'v*'], { cwd: root, encoding: 'utf8' }).split(/\r?\n/).filter(Boolean);
    console.log(JSON.stringify(releasePolicy(process.argv[2], tags)));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
