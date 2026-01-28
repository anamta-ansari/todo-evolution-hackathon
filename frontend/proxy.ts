// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

// Define protected routes that require authentication
const protectedRoutes = ['/dashboard'];

export function middleware(request: NextRequest) {
  // For this demo, we'll allow all requests to pass through
  // In a real app with server-side authentication, you would validate the JWT token here
  // Since we're using client-side auth with localStorage, this check happens in the components

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*'], // Apply middleware to these routes
};