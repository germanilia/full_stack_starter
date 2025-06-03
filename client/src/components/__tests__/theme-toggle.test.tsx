import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { ThemeToggle } from '@/components/ui/theme-toggle';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

const ThemeToggleWithProvider = () => (
  <ThemeProvider>
    <ThemeToggle />
  </ThemeProvider>
);

describe('ThemeToggle', () => {
  beforeEach(() => {
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    document.documentElement.className = '';
  });

  it('renders theme toggle button', () => {
    render(<ThemeToggleWithProvider />);
    const button = screen.getByRole('button');
    expect(button).toBeInTheDocument();
  });

  it('cycles through themes when clicked', () => {
    render(<ThemeToggleWithProvider />);
    const button = screen.getByRole('button');

    // Initial state should be system (Monitor icon)
    expect(button).toHaveAttribute('title', 'Switch to light mode');

    // Click to go to light mode
    fireEvent.click(button);
    expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'light');

    // Click to go to dark mode
    fireEvent.click(button);
    expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'dark');

    // Click to go back to system mode
    fireEvent.click(button);
    expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'system');
  });

  it('applies theme class to document element', () => {
    render(<ThemeToggleWithProvider />);
    const button = screen.getByRole('button');

    // Click to set light theme
    fireEvent.click(button);
    expect(document.documentElement.classList.contains('light')).toBe(true);

    // Click to set dark theme
    fireEvent.click(button);
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });
});
