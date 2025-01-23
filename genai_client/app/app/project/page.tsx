import Link from "next/link";
import { cookies } from "next/headers";

import MainLayout from "@/app/_layout/MainLayout";

import { Project } from "../_models/project";

import { getProjects } from "../_utils/fetch/project";

export default async function Projects() {
  let projects: Project[] = [];

  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getProjects(access);
    if (res.ok) {
      projects = await res.json();
    }
  } catch (error) {
    console.log(error);
  }
  
  return (
    <MainLayout>
      <Link href="/project/new" className="btn block w-[150px] mb-5 ml-auto">New project</Link>
      Projects:
      <ul>
        {projects.map((project) => (
          <li className="text-white">
            <Link href={`/project/${project.id}`}>{project.title}</Link>
          </li>
        ))}
      </ul>
    </MainLayout>
  );
}
