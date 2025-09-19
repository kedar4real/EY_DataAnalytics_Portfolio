"""
Portfolio Deployment Script
===========================

Automated deployment script for the EY Data Analytics Portfolio.
Handles project setup, dependency installation, and deployment preparation.

Author: Data Analytics Portfolio for EY
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class PortfolioDeployer:
    """Handles portfolio deployment and setup"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.portfolio_dir = self.root_dir / "portfolio_website"
        
    def check_requirements(self):
        """Check if required tools are installed"""
        print("🔍 Checking requirements...")
        
        # Check Python
        try:
            python_version = subprocess.check_output([sys.executable, "--version"]).decode().strip()
            print(f"✅ Python: {python_version}")
        except:
            print("❌ Python not found")
            return False
        
        # Check pip
        try:
            subprocess.check_output([sys.executable, "-m", "pip", "--version"])
            print("✅ pip: Available")
        except:
            print("❌ pip not found")
            return False
        
        return True
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("\n📦 Installing dependencies...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_deployment_package(self):
        """Create a deployment package"""
        print("\n📁 Creating deployment package...")
        
        deployment_dir = self.root_dir / "deployment_package"
        
        # Remove existing deployment directory
        if deployment_dir.exists():
            shutil.rmtree(deployment_dir)
        
        # Create new deployment directory
        deployment_dir.mkdir()
        
        # Copy portfolio website
        portfolio_src = self.portfolio_dir
        portfolio_dst = deployment_dir / "portfolio_website"
        shutil.copytree(portfolio_src, portfolio_dst)
        
        # Copy project files
        projects = [
            "01_Financial_Risk_Analytics",
            "02_Supply_Chain_Optimization", 
            "03_Customer_Analytics",
            "04_ESG_Analytics"
        ]
        
        for project in projects:
            src = self.root_dir / project
            dst = deployment_dir / project
            if src.exists():
                shutil.copytree(src, dst)
        
        # Copy shared utilities
        shared_src = self.root_dir / "shared_utilities"
        shared_dst = deployment_dir / "shared_utilities"
        if shared_src.exists():
            shutil.copytree(shared_src, shared_dst)
        
        # Copy main files
        main_files = ["README.md", "requirements.txt"]
        for file in main_files:
            src = self.root_dir / file
            dst = deployment_dir / file
            if src.exists():
                shutil.copy2(src, dst)
        
        print(f"✅ Deployment package created at: {deployment_dir}")
        return deployment_dir
    
    def create_github_pages_config(self):
        """Create GitHub Pages configuration"""
        print("\n🌐 Creating GitHub Pages configuration...")
        
        # Create .nojekyll file for GitHub Pages
        nojekyll_file = self.root_dir / ".nojekyll"
        nojekyll_file.touch()
        
        # Create GitHub Pages workflow
        workflow_dir = self.root_dir / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = """name: Deploy Portfolio to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./portfolio_website
"""
        
        workflow_file = workflow_dir / "deploy.yml"
        workflow_file.write_text(workflow_content)
        
        print("✅ GitHub Pages configuration created")
    
    def create_netlify_config(self):
        """Create Netlify configuration"""
        print("\n🚀 Creating Netlify configuration...")
        
        netlify_config = {
            "build": {
                "publish": "portfolio_website",
                "command": "echo 'No build step required'"
            },
            "redirects": [
                {
                    "from": "/*",
                    "to": "/index.html",
                    "status": 200
                }
            ]
        }
        
        import json
        netlify_file = self.root_dir / "netlify.toml"
        netlify_file.write_text(f"""[build]
  publish = "portfolio_website"
  command = "echo 'No build step required'"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
""")
        
        print("✅ Netlify configuration created")
    
    def create_vercel_config(self):
        """Create Vercel configuration"""
        print("\n⚡ Creating Vercel configuration...")
        
        vercel_config = {
            "version": 2,
            "builds": [
                {
                    "src": "portfolio_website/**/*",
                    "use": "@vercel/static"
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "/portfolio_website/$1"
                }
            ]
        }
        
        import json
        vercel_file = self.root_dir / "vercel.json"
        vercel_file.write_text(json.dumps(vercel_config, indent=2))
        
        print("✅ Vercel configuration created")
    
    def run_tests(self):
        """Run basic tests on the portfolio"""
        print("\n🧪 Running portfolio tests...")
        
        # Test portfolio website files
        required_files = [
            "portfolio_website/index.html",
            "portfolio_website/styles.css", 
            "portfolio_website/script.js"
        ]
        
        for file_path in required_files:
            if not (self.root_dir / file_path).exists():
                print(f"❌ Missing file: {file_path}")
                return False
        
        # Test project files
        projects = [
            "01_Financial_Risk_Analytics/financial_risk_dashboard.py",
            "02_Supply_Chain_Optimization/supply_chain_dashboard.py",
            "03_Customer_Analytics/customer_analytics_dashboard.py",
            "04_ESG_Analytics/esg_dashboard.py"
        ]
        
        for project_file in projects:
            if not (self.root_dir / project_file).exists():
                print(f"❌ Missing project file: {project_file}")
                return False
        
        print("✅ All required files present")
        return True
    
    def generate_deployment_instructions(self):
        """Generate deployment instructions"""
        print("\n📋 Generating deployment instructions...")
        
        instructions = """
# 🚀 EY Data Analytics Portfolio - Deployment Instructions

## Quick Deploy Options

### 1. GitHub Pages (Recommended - Free)
1. Create a new GitHub repository
2. Upload all files to the repository
3. Go to Settings > Pages
4. Select source: Deploy from a branch
5. Choose main branch and /portfolio_website folder
6. Your site will be live at: https://yourusername.github.io/repository-name

### 2. Netlify (Easy - Free)
1. Go to https://netlify.com
2. Drag and drop the portfolio_website folder
3. Your site will be live immediately
4. Option to connect custom domain

### 3. Vercel (Fast - Free)
1. Go to https://vercel.com
2. Import your GitHub repository
3. Deploy automatically
4. Global CDN included

### 4. Traditional Hosting
1. Upload portfolio_website folder to your web host
2. Ensure index.html is in the root directory
3. Test all functionality

## Before Deploying

### Update Personal Information
- [ ] Replace "Kedar" with your name in index.html
- [ ] Update email, LinkedIn, GitHub URLs
- [ ] Add your photo to the about section
- [ ] Customize hero title and subtitle

### Test Everything
- [ ] Open index.html in browser
- [ ] Test all navigation links
- [ ] Verify contact form works
- [ ] Check mobile responsiveness
- [ ] Test all project links

### Performance
- [ ] Optimize images (use WebP format)
- [ ] Minify CSS and JavaScript
- [ ] Enable gzip compression
- [ ] Set up analytics tracking

## Project Links

Your portfolio showcases these projects:
1. **Financial Risk Analytics** - Risk assessment and compliance
2. **Supply Chain Optimization** - Operations research and cost optimization
3. **Customer Analytics** - ML-based segmentation and churn prediction
4. **ESG Analytics** - Sustainability metrics and reporting

## Support

For questions:
- Check individual project README files
- Review portfolio_website/README.md
- Test all functionality before deployment

Good luck with your EY application! 🎯
"""
        
        instructions_file = self.root_dir / "DEPLOYMENT_INSTRUCTIONS.md"
        instructions_file.write_text(instructions)
        
        print("✅ Deployment instructions created")
    
    def deploy(self):
        """Main deployment process"""
        print("🚀 EY Data Analytics Portfolio Deployment")
        print("=" * 50)
        
        # Check requirements
        if not self.check_requirements():
            print("❌ Requirements check failed")
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            print("❌ Dependency installation failed")
            return False
        
        # Run tests
        if not self.run_tests():
            print("❌ Tests failed")
            return False
        
        # Create deployment package
        deployment_dir = self.create_deployment_package()
        
        # Create deployment configurations
        self.create_github_pages_config()
        self.create_netlify_config()
        self.create_vercel_config()
        
        # Generate instructions
        self.generate_deployment_instructions()
        
        print("\n🎉 Deployment preparation complete!")
        print(f"📁 Deployment package: {deployment_dir}")
        print("📋 Check DEPLOYMENT_INSTRUCTIONS.md for next steps")
        print("\n🚀 Your portfolio is ready for EY!")
        
        return True

def main():
    """Main function"""
    deployer = PortfolioDeployer()
    success = deployer.deploy()
    
    if success:
        print("\n✅ Portfolio deployment successful!")
        print("🌐 Ready to impress EY recruiters!")
    else:
        print("\n❌ Deployment failed. Please check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
