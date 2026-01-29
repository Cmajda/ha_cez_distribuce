import resolve from '@rollup/plugin-node-resolve';
import typescript from '@rollup/plugin-typescript';
import terser from '@rollup/plugin-terser';

const isProd = process.env.NODE_ENV === 'production';

export default {
  input: 'src/index.ts',
  output: {
    file: 'dist/cez-hdo-card.js',
    format: 'es',
    sourcemap: !isProd,
    inlineDynamicImports: true,
  },
  plugins: [
    resolve(),
    typescript({
      tsconfig: './tsconfig.json',
    }),
    ...(isProd ? [terser({
      format: {
        comments: false,
      },
      compress: {
        pure_funcs: ['console.log', 'console.debug', 'console.warn'],
        drop_debugger: true,
      },
    })] : []),
  ],
};
