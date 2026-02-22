#!/usr/bin/env node
/**
 * Script to run the Todo App frontend with proper configuration
 */
const { exec, spawn } = require('child_process');
const path = require('path');

console.log('Starting Todo App frontend server...');
console.log('Checking if dependencies are installed...');

// Change to frontend directory
const frontendDir = path.join(__dirname);

// First, check if node_modules exists
const fs = require('fs');
const nodeModulesPath = path.join(frontendDir, 'node_modules');

if (!fs.existsSync(nodeModulesPath)) {
    console.log('Installing frontend dependencies...');
    const installProcess = spawn('npm', ['install'], {
        cwd: frontendDir,
        stdio: 'inherit',
        shell: true
    });

    installProcess.on('close', (code) => {
        if (code === 0) {
            console.log('Dependencies installed successfully!');
            startDevServer();
        } else {
            console.error(`npm install failed with code ${code}`);
        }
    });
} else {
    console.log('Dependencies already installed.');
    startDevServer();
}

function startDevServer() {
    console.log('\nStarting frontend development server...');
    console.log('Environment variables:');

    // Set environment variables for the frontend
    const env = {
        ...process.env,
        NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
        PORT: process.env.PORT || '3000'
    };

    console.log(`  NEXT_PUBLIC_API_URL: ${env.NEXT_PUBLIC_API_URL}`);
    console.log(`  PORT: ${env.PORT}`);

    const devProcess = spawn('npm', ['run', 'dev'], {
        cwd: frontendDir,
        stdio: 'inherit',
        shell: true,
        env: env
    });

    devProcess.on('error', (err) => {
        console.error('Failed to start frontend:', err.message);
    });

    console.log('\nFrontend server starting on http://localhost:3000');
    console.log('Press Ctrl+C to stop the server');
}