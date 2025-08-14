import React from 'react';
import { render, screen, act } from '@testing-library/react';
import App from './App';

it('renders task manager heading', async () => {
  await act(async () => {
    render(<App />);
  });
  const headingElement = screen.getByText(/📋 Task Manager/i);
  expect(headingElement).toBeInTheDocument();
});

it('renders add task button', async () => {
  await act(async () => {
    render(<App />);
  });
  const buttonElement = screen.getByRole('button', { name: /add task/i });
  expect(buttonElement).toBeInTheDocument();
});