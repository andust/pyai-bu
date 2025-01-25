import { cookies } from "next/headers";

import MainLayout from "@/app/_layout/MainLayout";

import { Project } from "../../_models/project";

import { getProject } from "../../_utils/fetch/project";
import { IdParams } from "@/app/types";
import EstimationToolForm from "../../_molecules/estimation-tool-form/EstimationToolForm";
import { Developer } from "@/app/_models/developer";
import { getDevelopers } from "@/app/_utils/fetch/developer";

export default async function ProjectDetail({ params }: IdParams) {
  const projectId = (await params).id || "";
  let project: Project | null = null;
  let developers: Developer[] = [];

  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getProject(access, projectId);
    if (res.ok) {
      project = await res.json();
    }
  } catch (error) {
    console.log(error);
  }

  try {
    const cookieStore = await cookies();
    const access = cookieStore.get("access")?.value ?? "";
    const res = await getDevelopers(access);
    if (res.ok) {
      developers = await res.json();
    }
  } catch (error) {
    console.log(error);
  }

  return (
    <MainLayout>
      {project && (
        <>
          <ul className="space-y-3 whitespace-break-spaces">
            <li>
              <strong className="text-lg">Title:</strong>
              <div className="bg-sky-500/25 p-2">{project.title}</div>
            </li>
            <li>
              <strong className="text-lg">Description:</strong>
              <div className="bg-sky-500/25 p-2">{project.description}</div>
            </li>
            <li>
              <strong className="text-lg">Complexity:</strong>
              <div className="bg-sky-500/25 p-2">{project.complexity}</div>
            </li>
          </ul>
          {project.estimation && (
            <div className="mt-10">
              <strong className="text-lg">Estimation:</strong>
              <div className="bg-stone-500/25 p-2 text-left color-table" dangerouslySetInnerHTML={{ __html: project.estimation.result }} />
            </div>
          )}
        </>
      )}
      <EstimationToolForm projectId={projectId} developers={developers} />
    </MainLayout>
  );
}
