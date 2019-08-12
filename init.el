;; -*- emacs-lisp -*-

(setq inhibit-startup-message t)

;; Todos:

;; Aliases

(defalias 'clr 'count-lines-region)
(defalias 'arm 'auto-revert-mode)
(defalias 'sql 'sql-oracle)

(defalias 'perl-mode 'cperl-mode)

;; Others

(setq system-name (replace-regexp-in-string "\\..*$" "" system-name))
(setq frame-title-format 
      (concat user-login-name "@" system-name ":%b" ))

(setq cperl-indent-level 4)

;; Windows and terminal specific code.
(cond 
 ((eq window-system 'w32)
  (setq shell-file-name "c:/cygwin/bin/bash.exe")
  )
 ((eq window-system 'ns)
  (setq mac-option-modifier nil)
  (setq mac-command-modifier 'meta)
  )
 ((eq window-system nil)
  (xterm-mouse-mode 1)
  )
 )

(put 'erase-buffer     'disabled nil)

(global-set-key [f2]   'kill-this-buffer)
(global-set-key [f9]   'next-error)
(global-set-key [C-f9] 'previous-error)
(global-set-key [clearline] 'end-of-buffer) ;; urxvt
(global-set-key [f11]  'ffap)

(define-key ctl-x-map [?\C-b] 'ibuffer)

(defvar bookmark-save-flag 1)

(require 'dired-x)

(add-hook 'dired-mode-hook
	  '(lambda () 
	     (setq dired-omit-files-p t)))

;; An alternative is "C-a C-k" or "C-x h DEL".
(add-hook 'comint-mode-hook
	  '(lambda ()
	     (local-set-key [C-f2] 'erase-buffer)))

(add-hook 'shell-mode-hook 'ansi-color-for-comint-mode-on)

(cua-mode t)
(iswitchb-mode t)
(show-paren-mode t)
(xterm-mouse-mode t)

;; Backups
(setq
   backup-by-copying t      ; don't clobber symlinks
   backup-directory-alist
    '(("." . "~/.emacs.d/backups"))    ; all files should go in one dir
    )

;; --- chmod for executable scripts ---
(when (fboundp 'executable-make-buffer-file-executable-if-script-p)
  (add-hook 'after-save-hook 
	    'executable-make-buffer-file-executable-if-script-p
	    ))

;; --- sql-interactive-mode ---
(require 'sql)
(setq sql-product 'oracle)
(add-hook 'sql-mode-hook 'sql-local-mode-hook)
(add-hook 'sql-interactive-mode-hook 'sql-local-interactive-mode-hook)
(setenv "NLS_LANG" "american_america.al32utf8")
(add-to-list 'process-coding-system-alist
	     '("sqlplus" . utf-8))

(defun sql-local-mode-hook ()
  (local-set-key   [f7] 'sql-send-buffer)
  (local-set-key   [f9] 'sql-local-show-user)
  (local-set-key [C-f9] 'sql-local-status)
  )

(defun sql-local-interactive-mode-hook ()
  (setq truncate-lines t)
  (local-set-key     [f9] 'sql-local-show-user)
  (local-set-key   [C-f9] 'sql-local-status)
  (local-set-key [S-C-f9] 'sql-column-widths)
  )

(defun sql-column-widths ()
  (interactive)
    (sql-send-string "
set pages 10000;
column table_name    format a30;
column segment_name  format a30;
column object_name   format a30;
"
)
  )

(defun sql-local-status (n)
  "Send useful statements to the sql interpreter:

  1 status from v$instance
  2 timestamp
  4 archive log list;
"
  (interactive "p")
  (cond ((eq n 1)
	 (sql-send-string 
	  " 
column it format a10;\n
column hn format a15;\n
column st format a10;\n 
column ds format a10;\n 
select instance_name it, host_name hn, status st, database_status ds 
from v$instance;"))
	((eq n 2)
	 (sql-send-string
	  "select to_char(systimestamp,'yyyy-mm-dd:hh24:mi:ss') \"sys time\" from dual;"))	
	((eq n 4)
	 (sql-send-string
	  "archive log list;"))
	))

(defun sql-local-show-user(num)
  (interactive "p")
  (sql-send-string "column name_at_database heading user@database;")
  (sql-send-string "
select lower(user || '@' || 
       (select substr(global_name,1,45) from global_name ))
        name_at_database
from dual;")
  )

(defun xterm ()
  (interactive)
  (let ((l))
    (setq l (list "xterm" nil 0 nil "-e" "/bin/bash"))
    (apply 'call-process l)
  ))

(defun dired-calc-bytes ()
  (interactive)
  (let (
	(fn (dired-get-filename))
	)
    (calc-bytes 
     (number-to-string
      (elt (file-attributes fn) 7)))
    ))

(defun calc-bytes(s)
  "Calculate bytes into kilo bytes, mega bytes, and giga bytes."
  (interactive "sValue:")
  (let ((n (string-to-number s)))
    (message "%.0f B -  %.0f KB - %.0f MB %6.3f GB" 
	     n
	     (/ n (* 1024))
	     (/ n (* 1024 1024))
	     (/ n (* 1024.0 1024 1024))
	     )))

(defun buffer-set-default-directory ( dir )
  "Sets the current directory to DIR for buffers that do not have a
file name associated. The function is indented for the w32 port to set
the login directory (~/) because on startup the default directory for
*scratch* and *Messages* are the emacs bin directory or the long
directory name that was set in the properties of a emacs icon."
  (save-excursion
    (let (
	  (list (buffer-list))
	  )
      (while list
	(set-buffer (car list))
	(if (eq buffer-file-name nil)
	    (setq default-directory dir)
	  )
	(setq list (cdr list))
	))))

(when window-system 'w32
      (buffer-set-default-directory "~/")
      )
