module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.cjs'],
  moduleNameMapper: {
    '\\.(css|less|scss|svg|png|jpg|jpeg)$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\.[jt]sx?$': ['babel-jest', { configFile: './babel.config.cjs' }],
  },
  testMatch: ['<rootDir>/src/__tests__/**/*.test.[jt]sx?'],
  collectCoverageFrom: [
    'src/components/**/*.{js,jsx}',
    'src/pages/**/*.{js,jsx}',
    'src/context/**/*.{js,jsx}',
    '!src/main.jsx',
  ],
}
