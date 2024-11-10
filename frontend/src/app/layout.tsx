'use client';
import DashboardLayout from '@/components/Layout/Dashboard';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <DashboardLayout>{children}</DashboardLayout>;
}
