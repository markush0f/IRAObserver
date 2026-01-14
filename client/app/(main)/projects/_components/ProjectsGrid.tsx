"use client";

import { motion } from "framer-motion";
import type { Project } from "@/types/project";
import ProjectCard from "./ProjectCard";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export default function ProjectsGrid({ projects }: { projects: Project[] }) {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="grid gap-6 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4"
    >
      {projects.map((project) => (
        <motion.div key={project.id} variants={item}>
          <ProjectCard project={project} />
        </motion.div>
      ))}
    </motion.div>
  );
}
