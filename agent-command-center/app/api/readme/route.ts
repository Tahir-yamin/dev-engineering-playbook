import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
    try {
        const readmePath = path.join(process.cwd(), 'README.md');
        const fileContents = fs.readFileSync(readmePath, 'utf8');
        return new NextResponse(fileContents);
    } catch (error) {
        return new NextResponse('README.md not found', { status: 404 });
    }
}
