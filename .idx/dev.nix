# To learn more about how to use Nix to configure your environment,
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use. Options are "stable-23.11" or "unstable".
  channel = "stable-23.11";

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.go
    pkgs.sudo
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.nodejs_20
    pkgs.nodePackages.nodemon
    pkgs.python311Packages.flask
    pkgs.python311Packages.gunicorn
    pkgs.python311Packages.requests
    pkgs.python311Packages.sqlalchemy
    pkgs.python311Packages.psycopg2
    pkgs.python311Packages.flask_sqlalchemy
    pkgs.python311Packages.flask_migrate
    pkgs.python311Packages.flask_wtf
    pkgs.python311Packages.flask_login
  ];

  # Sets environment variables in the workspace
  env = {
    # Example environment variable
    FLASK_ENV = "development";
    FLASK_APP = "app.py";
  };

  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "vscodevim.vim"
      # Add more extensions as needed
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
        web = {
          # Example: run "npm run dev" with PORT set to IDX's defined port for previews,
          # and show it in IDX's web preview panel
          command = ["npm" "run" "dev"];
          manager = "web";
          env = {
            # Environment variables to set for your server
            PORT = "$PORT";
          };
        };
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      onCreate = {
        # Example: install JS dependencies from NPM
        npm-install = "npm install";
      };
      # Runs when the workspace is (re)started
      onStart = {
        # Example: start a background task to watch and re-build backend code
        watch-backend = "npm run watch-backend";
      };
    };
  };
}