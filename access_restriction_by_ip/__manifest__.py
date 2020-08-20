# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Niyas Raphy(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Access Restriction By IP',
    'summary': """All Users Can Access His Account Only From Specified IP Address""",
    'version': '13.0.2.2',
    'description': """All Users Can Access His Account Only From Specified IP Address (Mobile APP included)""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'contributors': ['Oscar B. ob@todoo.co'],
    'website': 'https://www.cybrosys.com',
    'category': 'Technical Settings',
    'depends': ['base', 'mail', 'website'],
    'license': 'AGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/allowed_ips_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'demo': [],
}
