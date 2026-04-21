"""Generate Luca-Ștefan Tamaș CV as a professional PDF with visual polish."""

from fpdf import FPDF

# ── Colors ──
NAVY     = (43, 87, 151)
TEAL     = (14, 165, 160)
DARK     = (33, 37, 41)
GRAY     = (85, 85, 85)
LIGHT    = (140, 140, 140)
BLACK    = (0, 0, 0)
WHITE    = (255, 255, 255)
PILL_BG  = (232, 240, 250)   # Light blue pill background
PILL_TXT = (43, 87, 151)     # Navy pill text
BAND     = (248, 249, 250)   # Very light gray section band

FONT_DIR = "C:/Windows/Fonts/"


class CVPDF(FPDF):
    def __init__(self):
        super().__init__(format="letter")
        self.set_auto_page_break(auto=True, margin=12)
        self.add_font("Calibri", "", FONT_DIR + "calibri.ttf")
        self.add_font("Calibri", "B", FONT_DIR + "calibrib.ttf")
        self.add_font("Calibri", "I", FONT_DIR + "calibrii.ttf")
        self.add_font("Calibri", "BI", FONT_DIR + "calibriz.ttf")

    # ── Top accent bar on each page ──
    def header(self):
        self.set_fill_color(*NAVY)
        self.rect(0, 0, self.w, 2.5, "F")
        self.set_fill_color(*TEAL)
        self.rect(self.w * 0.6, 0, self.w * 0.4, 2.5, "F")

    def section_title(self, text, icon=""):
        self.ln(2.5)
        label = f"{icon}  {text.upper()}" if icon else text.upper()
        self.set_font("Calibri", "B", 10)
        self.set_text_color(*NAVY)
        self.cell(0, 5, label, new_x="LMARGIN", new_y="NEXT")
        y = self.get_y()
        # Gradient-ish line: navy then teal
        mid = self.l_margin + (self.w - self.l_margin - self.r_margin) * 0.6
        self.set_draw_color(*NAVY)
        self.set_line_width(0.5)
        self.line(self.l_margin, y, mid, y)
        self.set_draw_color(*TEAL)
        self.line(mid, y, self.w - self.r_margin, y)
        self.ln(2)

    def job_header(self, title, company, dates, location):
        self.ln(1.5)
        self.set_font("Calibri", "B", 9.5)
        self.set_text_color(*DARK)
        title_w = self.get_string_width(title + "  |  ")
        self.cell(title_w, 4.5, title + "  |  ", new_x="RIGHT")
        self.set_text_color(*NAVY)
        self.cell(self.get_string_width(company), 4.5, company, new_x="RIGHT")
        self.set_font("Calibri", "", 8.5)
        self.set_text_color(*LIGHT)
        self.cell(0, 4.5, dates, align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Calibri", "I", 7.5)
        self.cell(0, 3, location, new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def bullet(self, text):
        self.set_font("Calibri", "", 8.5)
        self.set_text_color(*DARK)
        indent = 4
        bullet_w = 3.5
        self.cell(indent, 3.8, "")
        # Teal bullet
        self.set_text_color(*TEAL)
        self.set_font("Calibri", "B", 9)
        self.cell(bullet_w, 3.8, "\u2022 ")
        self.set_font("Calibri", "", 8.5)
        self.set_text_color(*DARK)
        self.multi_cell(
            self.w - self.l_margin - self.r_margin - indent - bullet_w,
            3.8, text, new_x="LMARGIN", new_y="NEXT"
        )
        self.ln(0.2)

    def bullet_tech_line(self, prefix, tech_text, highlight_text):
        self.set_text_color(*DARK)
        indent = 4
        bullet_w = 3.5
        self.set_font("Calibri", "B", 9)
        self.set_text_color(*TEAL)
        self.cell(indent, 3.8, "")
        self.cell(bullet_w, 3.8, "\u2022 ")

        self.set_font("Calibri", "B", 8.5)
        self.set_text_color(*DARK)
        self.cell(self.get_string_width(prefix), 3.8, prefix)
        self.set_font("Calibri", "", 8.5)
        self.cell(self.get_string_width(tech_text), 3.8, tech_text)
        self.set_font("Calibri", "B", 8.5)
        self.set_text_color(*TEAL)
        self.multi_cell(0, 3.8, highlight_text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*DARK)
        self.ln(0.2)

    def skill_pills(self, category, items):
        """Render skills as category label + inline pills."""
        self.set_font("Calibri", "B", 8.5)
        self.set_text_color(*NAVY)
        cat_text = category + ":"
        cat_w = self.get_string_width(cat_text) + 2
        self.cell(cat_w, 4.5, cat_text)

        self.set_font("Calibri", "", 7.5)
        for i, item in enumerate(items):
            item_text = f" {item} "
            w = self.get_string_width(item_text) + 2
            # Wrap to next line if needed
            if self.get_x() + w > self.w - self.r_margin:
                self.ln(5)
                self.cell(cat_w, 4.5, "")  # indent continuation
            x = self.get_x()
            y = self.get_y()
            # Pill background
            self.set_fill_color(*PILL_BG)
            self.rect(x, y + 0.3, w, 3.8, "F")
            # Pill text
            self.set_text_color(*PILL_TXT)
            self.cell(w, 4.5, item_text)
            self.cell(1.2, 4.5, "")  # gap between pills
        self.ln(5)

    def inline_certs(self, items):
        x_start = self.l_margin
        self.set_x(x_start)
        line_parts = []
        for i, (name, issuer) in enumerate(items):
            if i > 0:
                line_parts.append(("   |   ", "", LIGHT))
            line_parts.append((name, "B", DARK))
            line_parts.append((" \u2014 " + issuer, "", GRAY))
        for text, style, color in line_parts:
            self.set_font("Calibri", style, 8.5)
            self.set_text_color(*color)
            w = self.get_string_width(text)
            if self.get_x() + w > self.w - self.r_margin:
                self.ln(4)
                self.set_x(x_start)
            self.cell(w, 4, text)
        self.ln(4)


def build_cv():
    pdf = CVPDF()
    pdf.set_margin(15)
    pdf.add_page()

    # ═══════════════════════════════════════
    # HEADER
    # ═══════════════════════════════════════
    pdf.ln(1)
    pdf.set_font("Calibri", "B", 18)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 8, "LUCA-ȘTEFAN TAMAȘ", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Calibri", "", 9.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4.5, "Senior Full-Stack Engineer  \u00b7  System Design  \u00b7  SaaS Builder", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(0.5)
    pdf.set_font("Calibri", "", 7.5)
    pdf.set_text_color(*LIGHT)
    pdf.cell(0, 3.5,
        "lucastefantamasdev@gmail.com   \u00b7   +40 734 950 060   \u00b7   github.com/LucaStefan112   \u00b7   LinkedIn   \u00b7   Iași, Romania \u2014 Open to Remote (EU/US)",
        align="C", new_x="LMARGIN", new_y="NEXT"
    )

    # Divider
    pdf.ln(1.5)
    y = pdf.get_y()
    mid = pdf.l_margin + (pdf.w - pdf.l_margin - pdf.r_margin) * 0.6
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.6)
    pdf.line(pdf.l_margin, y, mid, y)
    pdf.set_draw_color(*TEAL)
    pdf.line(mid, y, pdf.w - pdf.r_margin, y)
    pdf.ln(0.5)

    # ═══════════════════════════════════════
    # PROFESSIONAL SUMMARY
    # ═══════════════════════════════════════
    pdf.section_title("Professional Summary")
    pdf.set_font("Calibri", "", 8.5)
    pdf.set_text_color(*DARK)
    pdf.multi_cell(0, 3.8,
        "Full-stack engineer with 5+ years of experience designing, building, and owning production systems end-to-end. "
        "Currently engineering high-throughput detection pipelines at Bitdefender while simultaneously founding and building "
        "Mazely \u2014 a production SaaS indoor navigation platform with a 20+ entity graph-based data model, real-time pathfinding, "
        "and enterprise analytics. Proven track record of architecting multi-tenant SaaS platforms, leading technical decisions "
        "across teams, and shipping complex systems from zero to production. Seeking Senior Engineer or Tech Lead roles where "
        "I can drive system design, own architecture, and deliver measurable business impact.",
        new_x="LMARGIN", new_y="NEXT"
    )

    # ═══════════════════════════════════════
    # CORE SKILLS (as pills)
    # ═══════════════════════════════════════
    pdf.section_title("Core Skills")
    pdf.skill_pills("Languages", ["TypeScript", "JavaScript", "Python", "SQL", "C/C++", "Dart"])
    pdf.skill_pills("Frontend", ["React", "Next.js", "Angular", "Tailwind CSS", "Framer Motion", "SSR/SSG"])
    pdf.skill_pills("Backend", ["Node.js", "NestJS", "Express", "REST APIs", "Prisma ORM", "JWT Auth"])
    pdf.skill_pills("Data", ["PostgreSQL", "MongoDB", "Redis", "MySQL", "Kafka", "OpenSearch/ELK"])
    pdf.skill_pills("Infra", ["Docker", "Kubernetes", "Azure", "Vercel", "MinIO", "GitHub Actions", "TeamCity"])
    pdf.skill_pills("Design", ["Multi-Tenant SaaS", "Microservices", "Event-Driven", "RBAC", "Graph Models", "CI/CD"])

    # ═══════════════════════════════════════
    # PROFESSIONAL EXPERIENCE
    # ═══════════════════════════════════════
    pdf.section_title("Professional Experience")

    # — Bitdefender —
    pdf.job_header("Security Software Engineer", "Bitdefender", "Oct 2025 \u2014 Present", "Iași, Romania \u00b7 Hybrid")
    pdf.bullet("Engineered high-throughput network traffic analysis pipeline processing large-scale data streams for real-time device identification and anomaly detection across enterprise networks")
    pdf.bullet("Designed and implemented a detection rule engine combining statistical analysis with LLM-assisted automation, improving detection accuracy and reducing manual rule maintenance overhead")
    pdf.bullet("Built and maintained distributed backend services (Node.js, Python) integrated with Kafka for event streaming, Redis for caching, and MongoDB for persistent storage")
    pdf.bullet("Orchestrated containerized microservices on Kubernetes across multiple environments, ensuring high availability and zero-downtime deployments")
    pdf.bullet("Implemented end-to-end observability using OpenSearch/ELK, enabling real-time system monitoring, performance analysis, and proactive incident detection")
    pdf.bullet("Automated the detection rule lifecycle by training LLM agents to generate and validate rule updates within CI/CD pipelines")

    # — Mazely —
    pdf.job_header("Founder & Engineer", "Mazely (mazely.app)", "Mar 2026 \u2014 Present", "Iași, Romania")
    pdf.bullet("Founded and built Mazely, a production SaaS indoor navigation platform for institutional buildings (hospitals, universities, government facilities) \u2014 from concept to deployed product")
    pdf.bullet("Architected a graph-based spatial data model (20+ entities, 7 connection types) enabling multi-floor, multi-building pathfinding with accessibility constraints and real-time route optimization")
    pdf.bullet("Designed photo-guided navigation system: corridor frame sequences with directional indexing, checkpoint-based wayfinding, and QR-code entry points \u2014 zero app download required")
    pdf.bullet("Built a full analytics pipeline \u2014 navigation session tracking, step-by-step event logging, QR scan analytics, visitor feedback collection, and admin dashboard visualization")
    pdf.bullet("Engineered multi-tenant admin platform with RBAC, per-building branding, invitation-based access, category management, and data export capabilities")
    pdf.bullet("Implemented i18n architecture supporting 4 languages (EN, RO, FR, DE) with a context-based translation system")
    pdf.bullet_tech_line(
        "Stack: ",
        "Next.js 15, React 19, TypeScript, PostgreSQL, Prisma ORM, Docker, MinIO, Vercel  |  ",
        "187 source files, 62 automated tests, 500+ line schema"
    )

    # — Enovis —
    pdf.job_header("Full-Stack Developer", "Enovis Software", "Aug 2023 \u2014 Oct 2025", "Iași, Romania \u00b7 Hybrid")
    pdf.bullet("Led architecture and development of a multi-tenant SaaS platform integrating BI, ERP, DMS, and BPMS modules, serving as the primary technical decision-maker for system design")
    pdf.bullet("Designed a role-based access control (RBAC) authorization model with strict tenant isolation, supporting fine-grained permissions across organizational boundaries")
    pdf.bullet("Architected backend services using NestJS and PostgreSQL with Prisma ORM, designing normalized schemas for complex business domains with migration-based deployments")
    pdf.bullet("Built production frontend applications with Next.js, implementing server-side rendering, state management, and responsive UX across devices")
    pdf.bullet("Established CI/CD pipelines with automated testing, static analysis, dependency scanning, and streamlined deployment workflows")
    pdf.bullet("Introduced system design review practices for new features, evaluating architecture trade-offs, integration patterns, and cross-service dependencies")
    pdf.bullet("Implemented comprehensive audit logging and monitoring for business-critical workflows, enabling traceability and incident investigation")

    # — Aperio —
    pdf.job_header("Security R&D Engineer", "Aperio Intelligence", "Aug 2024 \u2014 Jul 2025", "Remote \u00b7 United Kingdom")
    pdf.bullet("Designed and built a centralized authentication and authorization platform supporting multiple services \u2014 RBAC, JWT token management, secure session handling, and invitation-based onboarding")
    pdf.bullet("Engineered a payment processing service with end-to-end encryption, secure secret management (Azure Key Vault), and compliance-aware billing workflows")
    pdf.bullet("Deployed and operated cloud-native solutions on Microsoft Azure \u2014 managed identities, network segmentation, logging/monitoring, and least-privilege IAM policies")
    pdf.bullet("Owned full-stack features end-to-end (database \u2192 API \u2192 UI) using Node.js, TypeScript, and PostgreSQL")

    # — Codefy —
    pdf.job_header("Full-Stack Developer", "Codefy Software", "Feb 2022 \u2014 Sep 2024", "Iași, Romania")
    pdf.bullet("Developed and shipped web applications for clients in hospitality and marketplace sectors, from requirements to production deployment")
    pdf.bullet("Built responsive frontends with React and Angular; designed and implemented backend services with Node.js and Express")
    pdf.bullet("Designed and optimized PostgreSQL and MySQL databases for performance, scalability, and data integrity; collaborated across teams using Jira, Confluence, and Bitbucket")

    # — Freelance —
    pdf.job_header("Full-Stack & Mobile Developer", "Freelance", "Jun 2020 \u2014 Feb 2022", "Iași, Romania")
    pdf.bullet("Delivered 10+ client projects end-to-end: requirements gathering \u2192 architecture \u2192 development \u2192 testing \u2192 deployment \u2192 post-launch support")
    pdf.bullet("Built cross-platform mobile apps with Flutter and native Android (Android Studio); web apps with React, Angular, and Node.js")
    pdf.bullet("Published apps on Google Play and Apple App Store; operated as sole developer owning all technical decisions and delivery")

    # ═══════════════════════════════════════
    # EDUCATION
    # ═══════════════════════════════════════
    pdf.section_title("Education")

    pdf.set_font("Calibri", "B", 9)
    pdf.set_text_color(*DARK)
    title_text = "Bachelor\u2019s Degree in Computer Science"
    pdf.cell(pdf.get_string_width(title_text), 4.5, title_text)
    pdf.set_font("Calibri", "", 8.5)
    pdf.set_text_color(*LIGHT)
    pdf.cell(0, 4.5, "2021 \u2014 2024", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Calibri", "", 8.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 3.5, "Alexandru Ioan Cuza University, Iași  \u2014  Software Development & Analysis, Database and Network Design",
             new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════
    # CERTIFICATIONS
    # ═══════════════════════════════════════
    pdf.section_title("Certifications")
    pdf.inline_certs([
        ("Meta Data Analyst", "Meta"),
        ("Business Intelligence", "Google"),
        ("Advanced Tableau", "CFI"),
    ])
    pdf.inline_certs([
        ("Advanced SQL", "Kaggle"),
        ("Data Cleaning", "Kaggle"),
        ("AI Ethics", "Kaggle"),
    ])
    pdf.inline_certs([
        ("DevSecOps (THM-0D2ACJQ9DS)", "TryHackMe"),
    ])
    pdf.inline_certs([
        ("Security Engineer, Jr Penetration Tester, Cyber Security 101, Web Fundamentals, Pre Security", "TryHackMe"),
    ])

    # ═══════════════════════════════════════
    # LANGUAGES
    # ═══════════════════════════════════════
    pdf.section_title("Languages")
    pdf.set_font("Calibri", "B", 8.5)
    pdf.set_text_color(*DARK)
    pdf.cell(pdf.get_string_width("Romanian "), 4, "Romanian ")
    pdf.set_font("Calibri", "", 8.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(pdf.get_string_width("(Native)   |   "), 4, "(Native)   |   ")
    pdf.set_font("Calibri", "B", 8.5)
    pdf.set_text_color(*DARK)
    pdf.cell(pdf.get_string_width("English "), 4, "English ")
    pdf.set_font("Calibri", "", 8.5)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 4, "(C2 \u2014 Full Professional Proficiency)", new_x="LMARGIN", new_y="NEXT")

    # ── Output ──
    output_path = "C:/Projects/CV/Luca_Stefan_Tamas_CV.pdf"
    pdf.output(output_path)
    print(f"CV generated: {output_path}")
    print(f"Pages: {pdf.pages_count}")


if __name__ == "__main__":
    build_cv()
