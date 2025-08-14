import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from './App';

test('renders task manager heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/📋 Task Manager/i);
  expect(headingElement).toBeInTheDocument();
});

test('renders add task button', () => {
  render(<App />);
  const buttonElement = screen.getByRole('button', { name: /add task/i });
  expect(buttonElement).toBeInTheDocument();
});
