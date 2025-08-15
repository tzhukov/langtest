import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

it('renders task manager heading', () => {
  render(<App />);
  const headingElement = screen.getByText('Task Manager');
  expect(headingElement).toBeInTheDocument();
});

it('renders add task button', () => {
  render(<App />);
  const buttonElement = screen.getByRole('button', { name: 'Add Task' });
  expect(buttonElement).toBeInTheDocument();
});